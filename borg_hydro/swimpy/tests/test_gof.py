#!/usr/bin/python
# show commands being executed, per debug
#
######################################################################

#       Filename: test_gof.py

#       Author: Stefan Luedtke

######################################################################

from borg_hydro.swimpy import gof_python
import pandas as pd
import numpy as np
import pytest

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


def test_log_rmse_some_zeros(obs_some_zeros, sim_some_zeros):
    ''' Use the DataFrame with only ones to test and a single 0'''
    lrmse = gof_python.log_rmse(obs_some_zeros, sim_some_zeros)
    assert lrmse == 0


def test_nse_some_zeros(obs_some_zeros, sim_some_zeros):
    ''' Use the DataFrame with only ones to test and a single 0'''
    nse = gof_python.nse(obs_some_zeros, sim_some_zeros)
    assert pytest.approx(nse, 0.001) == -3.307692


def test_nse(obs_simple, sim_simple):
    ''' Use the DataFrame with only ones to test'''
    nse = gof_python.nse(obs_simple, sim_simple)
    assert np.isnan(nse)
