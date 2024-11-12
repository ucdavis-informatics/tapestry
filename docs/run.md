# TAPESTRY Installation and execution instructions

TAPESTRY is python based, built on Docker, and configuration driven.  It contains 2 products:

1. Data Ingestion and Derivation - A TAPESTRY configuration file defines the process of ingesting data from known or unkown sources, cleaning it, and deriving new information
1. Data display and annotation - In a second phase of effort, you can copy our boilerplate dashboard and configure it for the specifics of your data.  While this will take more coding than the first phase, the boilerplate offered here will provide a launch pad to visulization that will save you significant time and effort.

The rest of this documentation will walk you through:

- Understanding the TAPESTRY runtime, managed by Docker
- Configuring a TAPESTRY configuration file for data ingestion and derivation
- Tips for taking the boilerplate dashboard and configuring it to your data

---

## TAPESTRY runtime environment

TAPESTRY is packaged with a docker runtime environment in an effort to reduce portability challenges.  If you would like to review the environment, inspect the following files:

1. Dockerfile - defines system level dependencies
1. requirements.txt - defines python dependencies

Files that require specification to your environment:

1. tnsnames.ora - You should populate this file with Oracle TNS entries for your environment
1. .env - You will need to create this file.  Two examples have been provided.  One for UCDHS users, and one for everyone else
1. my_secrets.py - If you don't have an instance of [Hashicorp Vault]() or [BeyondTrust SecretSafe]() you can use this local approach to store your secrets in a file that is excluded from version control

### Setting up your TAPESTRY Environment

For documetation efficiency, this section is very opinionated about the use of VSCode - its just easiest to package all the functionality together.  However, there is no reason you can't use an alternative editor but, these docs will not address that.

1. Download and install [VSCode](https://code.visualstudio.com)
2. Download and install [Docker](https://www.docker.com)
3. Using the Extensions workflow in VSC, install the following extenstions:
    - Remove Development extension pack

4. Clone the repo
    - If you are at UCDHS, get clone link from [here](https://hc2-gitlab.ucdmc.ucdavis.edu/ri/pytdap/ucd-ri-pytdap)
    - If you are not employed with UCDHS, we can only release the OMOP version publicly, which you can access [here]()
        - If your institution uses Epic and you are Epic Certified, we are happy to share the [data adapters](data.md#data-sources) for Clarity and *Caboodle

5. Open the repo in VSC
    - when prompted, click reopen in container
    - If you are not prompted open the command tray (shift+ctrl+p on windows or shift+cmd+p on mac) and select 'reopen in container'


6. Review and run the packaged examples.  The examples are not meant to be clinically meaningful.  They are only provided to give a clear example of all the steps involved in creating a dataset with TAPESTRY.

7. Consider creating a TAPESTRY instance of your own by:
    - Copying and modifying the TAPESTRY configuration file
    - Copying and modifying and 'executor' script

---

## Data Ingestion and Derivation

This step is all about creating a configuration that instructs the TAPESTRY code to do 5 things:

1. Ingest data from a known clinical source (Epic Clarity, OMOP, etc...)
1. Ingest data from custom sources with bring your own code through an interface - Extenstions
1. Cleanup the data in matrix - Cleanups
1. Derive new information by combinging data together over time - Derivation
1. Save the results to a database

### Managing the TAPESTRY config file

See [Appendix A](#apendix-a) for an example TAPESTRY configuration file for OMOP

The most important keys are:

1. period - which sets the level of temporal resolution
    - minute
    - hour
    - day
    - week
    - month
1. databases - Which instructs TAPESTRY where to find connection information for your database that gets injected into the config at runtime - this is so you can share the config file without sharing your DB secrets!  Options include.  Techincally, these options are made available to you via the tapestry.py :: inject_secrets_into_config() function - you should review this function to see how it works and see [here for more](#appendix-a---databases).  In pseudocode, it reads secret data from one of the following sources and injects it into the in-memory configuration file:
    - vault - for ingesting secrets from a hashicorp vault instance, with either a temp token or an approle token
    - btss - for ingesting secrets from a beyond trust secret safe instance, with a valid user account and api key
    - mysecrets - for ingesting from a my_secrets.py file (that you should treat like a .env file and exclude from code repositories or sharing)
1. Concepts - where all the clinical concepts you wish to include are defined.  See [tapestry concepts](data.md#tapestry-concepts) for more
1. Extenstions - configures how custom data can be injested from other databases you have access to but don't havea publically known schema - this is bring your own code. See [tapestry extenstions](data.md#extensions)
1. Cleanups - configures logic to clean up data in the matrix before you attempt to make conclusions from it - this is bring your own code.  See [tapestry cleanups](data.md#cleanups)
1. Derivations - configures the derviation of data into information - this bring your own codes See [tapestry derivations](data.md#derivations)


---

## Running the TAPESTRY data ingestion and derivation examples

> [!IMPORTANT]
> It is important that you have access to a datasource compatible with this framework for these examples to work.  As of 2024-11-11, this means either an Epic Clarity or OMOP database running on either Oracle or MSSQL

Add your database connection information into the TAPESTRY configuration and then run the examples in either:

1. Jupyter notebooks
1. From the command line

Both of these options are avaiable directly through VS code


### Examples by notebook

Directly within VSCode, open any of the following you wish to run:

1. 01a - TAPESTRY on Clarity.ipynb
1. 02a - TAPESTRY on OMOP.ipynb

And step through the notebook executing each cell.

### Examples on the command line

Run any of the following commands to run the examples using the build in terminal within VSCode.  We encourage you  to review the well documented code to see whats taking place:

#### OMOP

```sh
python example_omop_executor.py --dotenv_file_path .env --config_key dev_omop --write_to_db true --pat_limit 10
```

#### Clarity

```sh
python example_clarity_executor.py --dotenv_file_path .env --config_key dev_clarity --write_to_db true --pat_limit 10
```


---

## Adding your own extensions/cleanups/derivations

These workflows are intended to be bring your own code, allowing you to inejct your own custom logic into the data ingestion, cleanup, or derivation phase of the TAPESTRY execution.  This is accomplished by supporting three simple interfaces in the TAPESTRY codebase combined with clear and concise configuration stanzas which allow you to have your modules called at runtime.


### Step 1 - write your module

All extension/clean-up/derivation code needs to be implemented as a seperate module.  So if you wanted to implement 3 derivations, you should create 3 new python files.  The name of the python file is injected into the configuration so TAPESTRY knows how to find it at runtime.  It is important that your modules be direct siblings of the executor file you are using to run TAPESTRY

Below is a brief discussion about how each of these works from a technical perspective

TAPESTRY will call each of your configured Extensions, Cleanups and Derivations with the call signatures below.  You must write your module to contain a function named, extend, cleanup, or derive respectively with these signatures

1. matrix_df - this is the primary matrix of data, [descrived here](data.md#tapestry-matrix)
1. data_manager.pat_profile_dict - This contains all patient identifiers, demographics, and a complete of list of this patients encounters during the time window you have configured for this patient
1. output_metadata - this is a mutable dictionary of key:value pairs that match each column in the matrix_df to a SQL datatype so that it can be correctly written to the database.  As you add columns from matrix_df, you must add a datatype description to this dictionary for each one
1. config - This is the arbitrary config dictionary you define for this module in the TAPESTRY config file - see immediately below.  At run time the entire TAPESTRY main config is added to this dictionary to give you access to it within your module
1. add_phase_func - the add phase func creates a running tablulation of every time a data value changes in the matrix.  This allows you to later group data up into phases, which can help you compress the matrix for easier seconary re-use.  We make this function available everywhere.


#### Extensions

The extension module exposes 3 additional internal TAPESTRY functions:

1. key_time_to_period - this normalizes incoming timestamps to the sampe time period as the matrix, set in your configuration file
1. get_mode_1 - If downsampling is required, this fucntion will help you derive the mode of your data upon grouping and aggregation.  Included purely as a helper
1. fill_concept_data_frame - This method exposes the built in logic to fill the concept dataframe from sparse to dense, which can be valuable depending on your use-case

```py
def extend(matrix_df, data_manager.pat_profile_dict, output_metadata, config, logger_name,
            to_period_func=key_time_to_period,
            mode_func = get_mode_1,
            fill_func=fill_concept_data_frame,
            add_phase_func=add_phase)
    """
        Extends TAPESTRY with additional conepts in a bring your own code approach
    """
    ...
```

#### Cleanups

```py
def cleanup(matrix_df, data_manager.pat_profile_dict, output_metadata, config, logger_name, add_phase_func=add_phase)
    """
    Cleans up and/or normalizes data in TAPESTRY for future use
    """
    ...
```

#### Derivations

```py
def derive(matrix_df, data_manager.pat_profile_dict, output_metadata, config, logger_name, add_phase_func=add_phase)
    """
    Derives new information based on concepts in TAPESTRY
    """
    ...
```

There are examples of all three of these in this repository for you to model your own implementations after.


### Step 2 - add your module to the TAPESTRY config file

There are 3 keys in the TAPESTRY configuration file that can take N children:

```py
{
    # rest of file above omitted for this example
    # extensions (may reference a data source in code)
    "extensions":{
        "example_extension_1":{
        "include": True or False,
        "module:" module name,
        "config":{
            "key 1":"value 1"
            }
        },
        "example_extension_2":{

        }
    },
    
    # cleanups
    "cleanups":{
        "example_cleanup_1":{
        "include": True or False,
        "module:" module name,
        "config":{
            "key 1":"value 1"
            }
        },
        "example_cleanup_2":{
            
        }
    },

    # derivations
    "derivations":{
        "example_derivation_1":{
        "include": True or False,
        "module:" module name,
        "config":{
            "key 1":"value 1"
            }
        },
        "example_derivation_2":{

        }
    },
}
```

All of these are defined with the same sub keys:

- include: True or False - allows you to toggle the module execution on or off
- module: module name - so if you have a derivation named 'derivation_bp.py'; the value here would be 'derivation_bp'
- config: an arbitrary dictionary of any key value pairs you wish to pass into the module.  This is extremely helpful if you need to instruct the module to use one of the databases you defined elsewhere in the config

All thats left is executing a TAPESTRY run with your configuration file!

## Creating your Executor script

This is final piece to implement a TAPESTRY data matrix.  I would hihgly encourge that you simply copy and modify on of the example executor scripts provided in this repository.  The code itself is well documented and will offer a straigh forward path to developing this component.

---
## Script Performance and parallelization

TAPESTRY can be run in either Serial or Parallel - the examples demo each.  To call it explicitly, you can think of TAPESTRY as embarassingly parallel.  It can be thought of as two nested for loops such that

- for each patient  
  - for each concept  
    - ingest data
  - extensions - add custom data with bring your own code - through the extensions interface
  - clean up data
  - derive new data

Since each patient is having the same set of operations applied, the parallelization examples demonstrate how to parallelize at the patient level.


---
## Data display and annotation

This step is all about leveraging the example dashboard template provided here and building in your own visualizations using the [Dash framework from Plotly](https://www.plotly.com)

The template is available in tapestry/data_display_and_annotation_example.  We suggest copying these files as good starting points since it comes pre-packaged with the following:

- A two page app with callbacks that offer easy navigation between the two.  The first page is a population overview.  The second page is a patient level deep dive
- A built in annotation workflow on the patient level page.  This allows data experts to click any point on any graph and add an annotation, closing the loop between data creators and data experts

---

## Apendix A

```py
"dev_omop":{
    ###############################
    # custom pcd tdap variables
    ###############################
    "alert_email":"test@test.com",
    "period":"H",
    "tables":{
        "matrix_table_name":"dev_omop_matrix"
    }, 
    #############################################
    # standard TDAP config items
    #############################################
    # data source secrets
    "databases":{
        "omop": {
            "type":"btss",
            "btss_secret_title":"testomopsql01_uchdw_omop_srv_cdi3",
            "sess_limit" : 25,
            "query_window_start" : 0,
            "query_window_end" : 24,
            "dest":False
        },
        "tdap_dm":{
                "type":"btss",
                "btss_secret_title":"edm_srv_tdap",
                "dest":True
            }
    },       

    "ts_features_config": {
        "window_len": 4,
        "window_type": "blackman",
        "fill_val": 0,
        "group_level": 0,
        "peak_order": 2,
        "peak_suffix": "_peak",
        "cp_model": "l2",
        "cp_min_size": 2,
        "cp_jump": 1,
        "cp_pen": 10,
        "cp_suffix": "_cp"
    },
    # concepts
    "concepts":{
        
        # "38176-4,36916-5,38176-4"
        "testmsr": {
            "conceptproperties": {
                "originid":[3034860,3034597],
                "origindatatype": "numeric",
                "origintype": "measurement",
                "desttable": "dev_omop_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },
        "testdx": {
            "conceptproperties": {
                "originid":[45596549, 35207173, 35211350],
                "origindatatype": "string",
                "origintype": "condition_occurrence",
                "desttable": "dev_omop_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },

        "testrx": {
            "conceptproperties": {
                "originid":[40164897, 36250141],
                "origindatatype": "string",
                "origintype": "drug_exposure",
                "desttable": "dev_omop_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },

        "testproc": {
            "conceptproperties": {
                "originid":[4133311,762510],
                "origindatatype": "string",
                "origintype": "procedure_occurrence",
                "desttable": "dev_omop_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },

        "testobs": {
            "conceptproperties": {
                "originid":[4353936],
                "origindatatype": "numberic",
                "origintype": "observation",
                "desttable": "dev_omop_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        }
        
    },

    "extensions":{},
    "derivations":{},
    "cleanups":{},   

} 
```


### Appendix A - databases

Three examples of adding an OMOP database to the 'databases' stanza of a TAPESTRY configuration file.  In each of the following cases this input is read by the tapestry function inject_secrets_into_config and the config is updated with the secret information that would be innapropriate for a shareable configuration file.  This data is injected into an in-memory version of the configuration which gets destroyed when the script exits.

To get specific, after these are processed by inject_secrets_into_config, they will have an extra key in them named 'secret' that contains the information needed to actually forge a connection to the database - see the [example_my_screts.py](../example_my_secrets.py) file for an example of what would be injected.

```py
# Configuring a database to use vault to obtain connection details
# Key points
# type = 'vault'
# vault must exists and contain the path to the secret in Vault
"omop": {
            "type":"vault",
            "vault_path":"<path/to/secret/in/vault>",
            "sess_limit" : 25,
            "query_window_start" : 0,
            "query_window_end" : 24,
            "dest":False
        }
```


```py
# Configuring a database to use beyond trust secret safe to obtain connection details
# Key points
# type = 'btss'
# btss_secret_title must exists and reference the title of the secret with your db connection details
"omop": {
            "type":"btss",
            "btss_secret_title":"<title in secret safe>",
            "sess_limit" : 25,
            "query_window_start" : 0,
            "query_window_end" : 24,
            "dest":False
        }
```


```py
# Configuring a database to use my_secrets dot pie to obtain connection details
# Key points
# Your connection details are stored in file named 'my_secrets.py'
# Please see 'example_my_secrets.py' for an example of what the file must contain.  There is an example for both Oracle and MSSQL
# You must pass in the secrets dictionary from your my_secrets.py file into the TAPESTRY function inject_secrets_into_config
"omop": {
            "type":"secretsdotpy",
            "key":"Dictionary key that contains the connection details for this database",
            "sess_limit" : 25,
            "query_window_start" : 0,
            "query_window_end" : 24,
            "dest":False
        }
```