#!/usr/bin/python
# show commands being executed, per debug
#
######################################################################

#       Filename: test_utils.py

#       Author: Stefan Luedtke

######################################################################

import pytest
import pandas as pd
from swimpy import utils

######################################################################


# Testing the path for the observed file
def test_obs():
    obs_file = r'./tests/test_data_gof/runoff_gof.dat'
    obs = utils.read_observed(obs_file)
    assert isinstance(obs, pd.DataFrame), 'Wrong data type'


# Testing the path for the simulated file
def test_sim():
    sim_file = r'./tests/test_data_gof/mc_results/stat_dis_out_0001.csv'
    sim = utils.read_simulated(sim_file)
    assert isinstance(sim, pd.DataFrame), 'Wrong data type'


######################################################################
# test the get_functions function- that one is crucial and quite tricky because
# we try to catch module and function name depending on the scope.
def test_get_function(config_obj):
    for item in config_obj.objectives:
        temp = utils.get_functions(item)
        assert (len(temp) == 3)
        for func in list(temp.values()):
            assert callable(func['exe']), 'The function is not callable'


def test_get_function_mo(config_mo_obj):
    for item in config_mo_obj.objectives:
        temp = utils.get_functions(item)
        assert (len(temp) == 3)
        for func in list(temp.values()):
            assert callable(func['exe']), 'The function is not callable'


def test_get_function_global(global_module_obj):
    for item in global_module_obj.objectives:
        print(item)
        temp = utils.get_functions(item)
        assert (len(temp) == 3)
        for func in list(temp.values()):
            assert callable(func['exe']), 'The function is not callable'


def test_get_function_multi(multi_station_obj):
    for item in multi_station_obj.objectives:
        print(item)
        temp = utils.get_functions(item)
        assert (len(temp) == 3)
        for func in list(temp.values()):
            assert callable(func['exe']), 'The function is not callable'
