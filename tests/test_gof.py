#!/usr/bin/python
# show commands being executed, per debug
#
######################################################################

#       Filename: test_gof.py

#       Author: Stefan Luedtke

######################################################################

import pytest
import datetime
import pandas as pd
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
    print(temp)
    assert isinstance(temp, pd.DataFrame), 'Wrong data type'


@pytest.fixture
def obs_simple():
    ''' Creating 2 DataFrame with with the same entry at every timestep'''
    todays_date = datetime.datetime.now().date()
    date = pd.date_range(todays_date-datetime.timedelta(10), periods=14,
                         freq='D')
    columns = ['X10', 'station']
    obs_simple = pd.DataFrame(columns=columns)
    obs_simple['date'] = date
    obs_simple = obs_simple.fillna(1)
    return(obs_simple)


@pytest.fixture
def sim_simple():
    ''' Creating 2 DataFrame with with the same entry at every timestep'''
    todays_date = datetime.datetime.now().date()
    date = pd.date_range(todays_date-datetime.timedelta(10), periods=14,
                         freq='D')
    columns = ['X10', 'station']
    sim_simple = pd.DataFrame(columns=columns)
    sim_simple['date'] = date
    sim_simple = sim_simple.fillna(1)
    return(sim_simple)


@pytest.fixture
def obs_sim_merge(obs_simple, sim_simple):
    temp = gof_python.obs_sim_merge(obs_simple, sim_simple)
    return(temp)


def test_log_rmse(obs_simple, sim_simple):
    ''' Use the DataFrame with only ones to test'''
    lrmse = gof_python.log_rmse(obs_simple, sim_simple)
    assert lrmse == 0


# Test the  computation of the performance
# This is just  wrapper function that uses only arguments from the
# configuration file to compute the performance measure for each objective.
def test_compute_gof(config_setup, config_obj):
    temp = gof_python.compute_gof(config_setup, config_obj)
    assert (len(temp) == 2)


def test_compute_gof_mo(config_mo_setup, config_mo_obj):
    temp = gof_python.compute_gof(config_mo_setup, config_mo_obj)
    assert (len(temp) == 4)


def test_compute_gof_res(config_setup, config_obj):
    temp = gof_python.compute_gof(config_setup, config_obj)
    assert temp == pytest.approx(
        [0.72450915761519741, 1.2196478869306084]), 'Results do not match'


def test_compute_gof_global_module(global_module_obj, global_module_setup):
    temp = gof_python.compute_gof(
            global_module_setup, global_module_obj)
    assert temp[0], True


def test_compute_gof_multi_station(multi_station_obj, multi_station_setup):
    temp = gof_python.compute_gof(multi_station_setup, multi_station_obj)
    assert temp == pytest.approx(0.724966)


######################################################################
# test the get_functions function- that one is crucial and quite tricky because
# we try to catch module and function name depending on the scope.
def test_get_function(config_obj):
    for item in config_obj.objectives:
        temp = gof_python.get_functions(item)
        assert (len(temp) == 3)
        for func in list(temp.values()):
            assert callable(func['exe']), 'The function is not callable'


def test_get_function_mo(config_mo_obj):
    for item in config_mo_obj.objectives:
        temp = gof_python.get_functions(item)
        assert (len(temp) == 3)
        for func in list(temp.values()):
            assert callable(func['exe']), 'The function is not callable'


def test_get_function_global(global_module_obj):
    for item in global_module_obj.objectives:
        print(item)
        temp = gof_python.get_functions(item)
        assert (len(temp) == 3)
        for func in list(temp.values()):
            assert callable(func['exe']), 'The function is not callable'


def test_get_function_multi(multi_station_obj):
    for item in multi_station_obj.objectives:
        print(item)
        temp = gof_python.get_functions(item)
        assert (len(temp) == 3)
        for func in list(temp.values()):
            assert callable(func['exe']), 'The function is not callable'
