"""
Author: Bill Riedl
Date: 2024-10-26
Purpose: to have a packaged script that builds a TDAP matrix for testing and development purposes
"""

#####################
# imports and config
#####################
import argparse
import re
import pandas as pd
from random import sample
from tqdm import tqdm
from datetime import datetime
import distutils.util
import sys
import atexit
from pathlib import Path

# logging imports for multiprocess logging
import logging
from multiprocessing import Pool
from time import sleep

# ripy
from ucdripydbutils import ucdripydbutils
from piesafe import piesafe

# TDAP imports
from tapestry.tapestry import (get_concept_metadata,
                        run_omop,
                        print_cleanups,
                        print_extensions,
                        print_derivations,
                        print_concepts,
                        inject_secrets_into_config)

# sibling file imports
import example_tapestry_config as my_tdap_config


###########################################
# parser and other globals
###########################################
parser = argparse.ArgumentParser(
    description="Example TDAP arg parser"
)
parser.add_argument('--dotenv_file_path',
                    required=False,
                    help='The full path to the .env file. Defaults to ./.env',
                    default=Path.cwd() / '.env')

parser.add_argument('--config_key',
                    help='Chooses which configuration from tdap_config to use',
                    type=str,
                    required=True)

parser.add_argument('--write_to_db',
                    help='If True, write results to DB.  Else, dont',
                    type=lambda x:bool(distutils.util.strtobool(x)),
                    default=True)

parser.add_argument('--use_named_ad_auth_to_mssql',
                    help='If True, write results to DB.  Else, dont',
                    type=lambda x:bool(distutils.util.strtobool(x)),
                    default=False)

parser.add_argument('--build_number',
                    type=int,
                    help="Optional argument that, when passed, will result in the logfile being named to incldue this number",
                    default = 0)
# developer args
parser.add_argument('--pat_limit',
                    help='Number of patient records to limit processing to',
                    type=int,
                    default=10)

parser.add_argument('--dev_email',
                    help='The email to which failure notices should be sent',
                    type=str,
                    default='awriedl@ucdavis.edu')




#####################################
# tdap call funcs - serial or parallel
# the specific run function called is where the binding
# to a specicific data source is made
# in this case 'run_clarity'
#####################################
def get_omop_matrix_serial(data_tuple_list):
    ret_dict_list = []
    print(f"In get matrix serial, First Tuple is: {data_tuple_list[0]}")
    for one_tuple in tqdm(data_tuple_list):
        ret = run_omop(*one_tuple)
        ret_dict_list.append(ret)
    return ret_dict_list

def get_omop_matrix_parallel(data_tuple_list, process_count=4):
    with Pool(processes=process_count) as p:
        ret_dict_list = p.starmap(run_omop, data_tuple_list)
    return ret_dict_list


def get_pop(tdap_config, logger_name):
    """
    This function gets the population for processing
    """
    logger = logging.getLogger(logger_name)
    logger.info("Getting the population from OMOP")
    omop_engine = ucdripydbutils.get_engine_from_connect_dict(tdap_config.get('databases').get('omop').get('secret'))
    # get the population
    pop_sql = """
    SELECT TOP 50
        person_id,
        measurement_datetime as start_time
    FROM
        Measurement
    where
        measurement_concept_id in (3034860,3034597)

    UNION

    SELECT TOP 50
        person_id,
        condition_start_datetime as start_time
    FROM
        Condition_occurrence
    where
        condition_concept_id in (45596549, 35207173, 35211350)

    UNION

    SELECT TOP 50
        person_id,
        drug_exposure_start_datetime as start_time
    FROM
        Drug_exposure
    where
        drug_concept_id in (40164897, 36250141)   

    UNION

    SELECT TOP 50
        person_id,
        procedure_datetime as start_time
    FROM
        Procedure_occurrence
    where
        procedure_concept_id in (4133311,762510)

    UNION

    SELECT TOP 50
        person_id,
        observation_datetime as start_time
    FROM
        Observation
    where
        observation_concept_id in (4353936)    
    """
    pop_df = pd.read_sql(pop_sql, omop_engine)
    pop_df = pop_df.dropna()
    omop_engine.dispose()
    return pop_df


def create_process_df(df, logger_name):
    """
    This function creates a dataframe that sets the population for processing

    In the clarity version we support procesing by both pat_id and start/stop times OR pat_enc_csn_id(s)

    In this OMOP version we will only support processing by person_id and start/stop times

    """
    logger = logging.getLogger(logger_name)

    process_df = df.copy()
    process_df['end_time'] = process_df['start_time'] + pd.Timedelta(days=7)
    process_df['start_time_str'] = process_df['start_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    process_df['end_time_str'] = process_df['end_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    process_df['visit_occurrence_id_list'] = None
    process_df['id_type'] = 'person_id'

    return process_df


def run(tdap_config, write_to_db, logger_name, pat_limit, parallel=False):
    """
    This function is the main function that runs the TDAP process
    """
    logger = logging.getLogger(logger_name)
    logger.info("Starting the TDAP run")


    # get the population
    logger.info("Getting the population from OMOP")
    pop_df = get_pop(tdap_config, logger_name)
    logger.info(f"Population size: {pop_df.shape[0]}")

    # create the process_df
    logger.info("Creating a patient set with start and end times to feed population to TDAP")
    process_df = create_process_df(pop_df, logger_name)
    logger.info(f"Process_df size: {process_df.shape[0]}")
    process_tuples = list(process_df.filter(['person_id', 'start_time_str', 'end_time_str','visit_occurrence_id_list','id_type']).to_records(index=False))
    run_args_tuple = (tdap_config, logger_name, 'omop')
    process_tuples_final = [tuple(x) + run_args_tuple for x in process_tuples]
    logger.info(f"Process_tuples_final size: {len(process_tuples_final)}")
    if pat_limit > 0 and pat_limit < len(process_tuples_final):
        process_tuples_final = sample(process_tuples_final, pat_limit)
        logger.info(f"Processing limited to {pat_limit} patients")


    ##########################
    # TDAP - review whats about to be processed
    ##########################
    print_concepts(tdap_config, print_or_log='log', logger_name=logger_name)
    print_extensions(tdap_config, print_or_log='log', logger_name=logger_name)
    print_derivations(tdap_config, print_or_log='log', logger_name=logger_name)
    print_cleanups(tdap_config, print_or_log='log', logger_name=logger_name)


    if parallel:
        logger.info("Running TDAP on OMOP in parallel using {} processes".format(tdap_config.get('databases').get('omop').get('sess_limit')))
        ret_dict_list = get_omop_matrix_parallel(process_tuples_final, process_count=tdap_config.get('databases').get('omop').get('sess_limit'))
        logger.info("TDAP run complete")
    else:
        logger.info("Running TDAP on OMOP in serial")
        ret_dict_list = get_omop_matrix_serial(process_tuples_final)
        logger.info("TDAP run complete")
    

    if write_to_db:            
        for k,v in tdap_config.get('databases').items():
            if v['dest'] == True:
                start_time = datetime.now()
                # create an engine for output db
                logger.info("Now writing to {} database".format(k))
                connect_dict = v.get('secret')
                o_engine = ucdripydbutils.get_engine_from_connect_dict(connect_dict)
                print(pd.read_sql("select @@version", o_engine))
                ###############################
                ## do the writing here
                ###############################
                
                ## step 1 - obtain matrix metadata from tdap results and create a table
                # pcd_matrices
                meta_dict_list = [x['output_metadata'] for x in ret_dict_list]
                # find longest outputmetadata, use it as template for table creation
                tdap_output_table_metadata = max([x for x in meta_dict_list], key=len)
                # create empty table with template and persist to DB
                temp_matrix_df = pd.DataFrame(columns=tdap_output_table_metadata.keys())
                temp_matrix_df.to_sql(tdap_config['tables']['matrix_table_name']+'_temp', o_engine, dtype=tdap_output_table_metadata, index=False, if_exists='replace')

                matrix_df_list = [x['matrix_df'] for x in ret_dict_list]
                for matrix_df in matrix_df_list:
                    matrix_df.filter(tdap_output_table_metadata.keys()).to_sql(tdap_config['tables']['matrix_table_name']+'_temp', o_engine, dtype=tdap_output_table_metadata, index=False, if_exists='append')
                             
                # rename temp table to final table
                ucdripydbutils.rename_table_mssql(o_engine, tdap_config['tables']['matrix_table_name']+'_temp', tdap_config['tables']['matrix_table_name'], logger)

                o_engine.dispose()
                end_time = datetime.now()
                logger.info(f"Writing to {k} database took {end_time-start_time}")
    else:
        logger.info("TDAP run complete.  Results not written to DB")
        return ret_dict_list
    

#####################################
# main func
#####################################
def main():
    print("Hello, I'm PCD on tdap 2.0")
    try:
        # DO MAIN STUFF
        print("Hello, I'm TDAP on OMOP here to procees a test run for  you!!")
        args = parser.parse_args()
        config_key = args.config_key
        dotenv_file_path = args.dotenv_file_path
        write_to_db = args.write_to_db
        use_named_ad_auth_to_mssql = args.use_named_ad_auth_to_mssql
        build_number = args.build_number
        
        #dev args
        dev_email = args.dev_email
        pat_limit = args.pat_limit
       
       # logging setup
        logging_config = my_tdap_config.logging_config
        logger_name = 'tdap_logger'
        log_file_name = 'tdap.log'
        date_str = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
        log_file_name = log_file_name.split('.')[0]+'_'+date_str+'.'+log_file_name.split('.')[1]
        build_number = args.build_number
        if build_number > 0:
            print(f"Before build number log file name: {log_file_name}")
            splits = log_file_name.split('.')
            log_file_name = splits[0]+'_'+str(build_number)+'.'+splits[1]
            print(f"After build number log file name: {log_file_name}")
        # always dump logs into log/ directory
        log_file_name = 'log/'+log_file_name
        print(f"Final log file name is {log_file_name}")
        # update log file name in logging config
        logging_config['handlers']['file']['filename'] = log_file_name
                        
        logger = logging.getLogger(logger_name)
        logging.config.dictConfig(logging_config)
        logger.info("Logger is configured!!!")           
        
        ###########################
        # TDAP config management
        ###########################
        # check to see if user wants to use named AD credentials
        if use_named_ad_auth_to_mssql:
            ad_user = input("Enter AD username: ")
            ad_pass = input("Enter AD password: ")
        else:
            ad_user = None
            ad_pass = None
        tdap_config = my_tdap_config.tdap_configs.get(config_key)
        tdap_config['logging_config'] = logging_config
        # update tdap config with secrets
        # NOTE - if using mysecrets, be sure you have imported the file so that you can can include in the arguments here using my_secrets = mysecrets.my_secrets
        tdap_config = inject_secrets_into_config(dotenv_file_path, tdap_config, dev_email, logger_name, mssql_ad_user=ad_user, mssql_ad_pass=ad_pass)

        # call run
        run(tdap_config, write_to_db, logger_name, pat_limit)
    except Exception as e:
        if dev_email is not None:
            piesafe.failure_email(log_file_name, email_subject=f'Bad Exit from TDAP OMOP EXAMPLE', email_txt=f"{piesafe.exception_to_string(e)}",email_to=dev_email)
        logger.exception('------Traceback------')
        logger.error(e)
        sys.exit("\N{CRYING FACE}")
    finally:
        # complete
        logger.info("============== The call to run has completed ======================")


if __name__ == "__main__":
    main()