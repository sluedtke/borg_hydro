#!/usr/bin/python
# show commands being executed, per debug
#
######################################################################

#       Filename: test_gof.py

#       Author: Stefan Luedtke

######################################################################

import pytest
import pandas as pd
import numpy as np
from swimpy import gof_python

######################################################################


# Testing the path for the observed file
def test_obs():
    obs_file = r'./tests/test_data_gof/runoff_gof.dat'
    obs = gof_python.read_observed(obs_file)
    assert isinstance(obs, pd.DataFrame), 'Wrong data type'


# Testing the path for the simulated file
def test_sim():
    sim_file = r'./tests/test_data_gof/mc_results/stat_dis_out_0001.csv'
    sim = gof_python.read_simulated(sim_file)
    assert isinstance(sim, pd.DataFrame), 'Wrong data type'


@pytest.fixture()
def read_obs():
    ''' Just a fixture to read the files for further testing'''
    obs_file = r'./tests/test_data_gof/runoff_gof.dat'
    obs = gof_python.read_observed(obs_file)
    return(obs)


@pytest.fixture()
def read_sim():
    ''' Just a fixture to read the files for further testing'''
    sim_file = r'./tests/test_data_gof/mc_results/stat_dis_out_0001.csv'
    sim = gof_python.read_simulated(sim_file)
    return(sim)


# Merging observation and simulation into one datafram
def test_obs_sim_merge(read_obs, read_sim):
    temp = gof_python.obs_sim_merge(read_obs, read_sim)
    assert isinstance(temp, pd.DataFrame), 'Wrong data type'


# A fixture for merging observation and simulation into one dataframe
@pytest.fixture
def obs_sim_merge(read_obs, read_sim):
    temp = gof_python.obs_sim_merge(read_obs, read_sim)
    return(temp)


@pytest.fixture
def obs_simple(obs_sim_merge):
    ''' Creating 2 DataFrame with with the same entry at every timestep'''
    # Subset using only the first 10 columns
    obs_simple = pd.DataFrame(obs_sim_merge['obs'][0:10].copy())
    # Set all values to one
    obs_simple.loc[:, 'obs'] = np.array([1] * len(obs_simple))
    return(obs_simple)


@pytest.fixture
def sim_simple(obs_sim_merge):
    ''' Creating 2 DataFrame with with the same entry at every timestep'''
    # Subset using only the first 10 columns
    sim_simple = pd.DataFrame(obs_sim_merge['sim'][0:10].copy())
    # Set all values to one
    sim_simple.loc[:, 'sim'] = np.array([1] * len(sim_simple))
    return(sim_simple)


def test_log_rmse(obs_simple, sim_simple):
    ''' Use the DataFrame with only ones to test'''
    lrmse = gof_python.log_rmse(obs_simple, sim_simple)
    assert lrmse == 0


# Test the  computation of the performance
# This is just  wraopper function that uses only arguments from the
# configuration file to compute the performance measure for each objective.
def test_compute_gof(config_obj):
    temp = gof_python.compute_gof(config_obj)
    assert (len(temp) == 2)


def test_compute_gof_mo(config_mo_obj):
    temp = gof_python.compute_gof(config_mo_obj)
    assert (len(temp) == 4)


def test_compute_gof_res(config_obj):
    temp = gof_python.compute_gof(config_obj)
    assert temp == [0.72450915761519741, 1.2196478869306084], \
            'Results do not match'
