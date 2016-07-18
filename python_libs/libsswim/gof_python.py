#!/usr/bin/python
# show commands being executed, per debug
#
######################################################################

#       Filename: gof_python.py

#       Author: Stefan Luedtke

######################################################################

# How to read the observed runoff file??

import pandas as pd

def read_observed(obs_file):
    '''That function takes a single file name from the observed data and reads
    this as pandas data frame. Currently, only one single columns holds the data
    (the second one) and the first one is the date and index column.'''

    temp = pd.read_csv(obs_file, sep='\t', index_col='date',
                       parse_dates=['date'])
    return(temp)


def read_simulated(simu_file):
    '''That function takes a single file name from the simulated data and reads
    this as pandas data frame. Currently, only one single columns holds the data
    (the third one) and the first two the date and thus the index column.'''

    dateparse = lambda y, d: pd.datetime.strptime(''.join([y, d]), '%Y%j')

    temp = pd.read_csv(simu_file, sep='\t', index_col='date',
                       parse_dates={'date': ['YEAR', 'DAY']},
                       date_parser=dateparse)
    return(temp)
