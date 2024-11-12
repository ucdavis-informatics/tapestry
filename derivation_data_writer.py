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
    # write data to disk in pickle files or other
    return df, output_metadata
