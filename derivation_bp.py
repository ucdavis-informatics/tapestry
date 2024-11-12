"""
Author: Bill Riedl
Date: 2020-09-15
Purpose: BP data is stored as a string in Epic clarity.  Something like 110/70.  This function parses this string
and stores the systolic and diastolic components in their own columns and converts them to numbers
"""
# imports
from tdap.cleanup_utils import (col_check, MissingRequiredCols)
from sqlalchemy import types
import pandas as pd
import logging

# Create a BP derived MAP column
def derive(df, pat_profile_dict, output_metadata, config, logger_name, add_phase_func=None):
    logger = logging.getLogger(logger_name)
    if col_check(df, config.get('required_cols')):
        bpCols = ['bp_systolic','bp_diastolic']
        df[bpCols] = df[config.get('bp_source_col')].str.split('/',expand=True)
        df[bpCols] = df[bpCols].apply(pd.to_numeric,errors='coerce', axis=1)
        # Add bp_map col
        df['bp_map'] = round((0.3334*df['bp_systolic']) + (0.6667*df['bp_diastolic']))
        # update output metadata
        output_metadata['bp_systolic'] = types.Numeric(precision=5, scale=1)
        output_metadata['bp_diastolic'] = types.Numeric(precision=5, scale=1)
        output_metadata['bp_map'] = types.Numeric(precision=5, scale=1)
    else:
        logger.error("Input columns for BP cleanup not present...skipping!  This may cause problems with missing columns later!")
        raise MissingRequiredCols
    return df, output_metadata
