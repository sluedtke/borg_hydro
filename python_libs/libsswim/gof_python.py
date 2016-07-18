#!/usr/bin/python
# show commands being executed, per debug
#
######################################################################

#       Filename: gof_python.py

#       Author: Stefan Luedtke

######################################################################

import pandas as pd

######################################################################


# --------------------------
def read_observed(obs_file):
    '''That function takes a single file name from the observed data and reads
    this as pandas data frame. Currently, only a single columns holds the data
    (the second one) and the first one is the date and index column.'''

    temp = pd.read_csv(obs_file, sep='\t', index_col='date',
                       parse_dates=['date'])
    return(temp)


# ----------------------------
def read_simulated(simu_file):
    '''That function takes a single file name from the simulated data and reads
    this as pandas data frame. Currently, only a single columns holds the data
    (the third one) and the first two the date and thus the index column.'''

    dateparse = lambda y, d: pd.datetime.strptime(''.join([y, d]), '%Y%j')

    temp = pd.read_csv(simu_file, sep='\t', index_col='date',
                       parse_dates={'date': ['YEAR', 'DAY']},
                       date_parser=dateparse)
    return(temp)


# ---------------------------------------------
def window_ts(pandas_df, start_date, end_date):
    ''' This function takes a pandas dataframe, a start and an end date and
    returns the df starting with start_date and ending with end_date.'''
    # Create an index with the new date range
    temp_index = pd.date_range(start=start_date, end=end_date)
    # Use that index to clip the input data frame
    pandas_df = pandas_df.loc[temp_index]
    return(pandas_df)


# ----------------------------------------
def obs_sim_merge(pandas_obs, pandas_sim):
    ''' This function takes tow pandas dataframes and merges them into a single
    one. The new column names are "obs" and "sim". The join or merge will be
    based on the timestamp of the observed data set only and NA values will be
    dropped.'''
    temp = pd.concat([pandas_obs, pandas_sim], axis=1).dropna()
    temp.columns = ['obs', 'sim']
    return(temp)
