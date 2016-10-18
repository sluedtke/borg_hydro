#!/usr/bin/python
# show commands being executed, per debug
#
######################################################################

#       Filename: test_gof.py

#       Author: Stefan Luedtke

######################################################################

from swimpy import gof_python
import pandas as pd

######################################################################


# Merging observation and simulation into one datafram
def test_obs_sim_merge(read_obs, read_sim):
    temp = gof_python.obs_sim_merge(read_obs, read_sim)
    print(temp)
    assert isinstance(temp, pd.DataFrame), 'Wrong data type'


def test_log_rmse(obs_simple, sim_simple):
    ''' Use the DataFrame with only ones to test'''
    lrmse = gof_python.log_rmse(obs_simple, sim_simple)
    assert lrmse == 0
