#!/usr/bin/python
# show commands being executed, per debug
#
######################################################################

#       Filename: test_gof.py

#       Author: Stefan Luedtke

######################################################################
import pytest
import pandas as pd
from python_libs.libsswim import gof_python

######################################################################


# Testing the path for the observed file
def test_obs():
    obs_file = r'./runoff_gof.dat'
    obs = gof_python.read_observed(obs_file)
    assert isinstance(obs, pd.DataFrame), 'Wrong data type'


# Testing the path for the simulated file
def test_sim():
    sim_file = r'./mc_results/stat_dis_out_0001.csv'
    sim = gof_python.read_simulated(sim_file)
    assert isinstance(sim, pd.DataFrame), 'Wrong data type'


@pytest.fixture()
def read_obs():
    ''' Just a fixture to read the files for further testing'''
    obs_file = r'./runoff_gof.dat'
    obs = gof_python.read_observed(obs_file)
    return(obs)


@pytest.fixture()
def read_sim():
    ''' Just a fixture to read the files for further testing'''
    sim_file = r'./mc_results/stat_dis_out_0001.csv'
    sim = gof_python.read_simulated(sim_file)
    return(sim)


# Merging observation and simulation into one datafram
def test_obs_sim_merge(read_obs, read_sim):
    temp = gof_python.obs_sim_merge(read_obs, read_sim)
    assert isinstance(temp, pd.DataFrame), 'Wrong data type'
