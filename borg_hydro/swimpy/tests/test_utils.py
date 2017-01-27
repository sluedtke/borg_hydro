#!/usr/bin/python
# show commands being executed, per debug
#
######################################################################

#       Filename: test_utils.py

#       Author: Stefan Luedtke

######################################################################

import pytest
import filecmp
import pandas as pd
import numpy as np
import datetime
from borg_hydro.swimpy import utils

######################################################################


# Testing the path for the observed file

def test_obs():
    obs_file = r'./borg_hydro/swimpy/tests/test_input/runoff_gof.dat'
    obs = utils.read_observed(obs_file)
    assert isinstance(obs, pd.DataFrame), 'Wrong data type'


# Testing the path for the simulated file
def test_sim():
    sim_file = r'./borg_hydro/swimpy/tests/test_output/Res/stat_dis_out_0001.csv'
    sim = utils.read_simulated(sim_file)
    assert isinstance(sim, pd.DataFrame), 'Wrong data type'


######################################################################
# test the get_functions function- that one is crucial and quite tricky because
# we try to catch module and function name depending on the scope.

def test_get_function(config_setup):
    for item in config_setup.objectives:
        temp = utils.get_functions(item)
        assert (len(temp) == 3)
        for func in list(temp.values()):
            assert callable(func['exe']), 'The function is not callable'


def test_get_function_mo(config_mo_setup):
    for item in config_mo_setup.objectives:
        temp = utils.get_functions(item)
        assert (len(temp) == 3)
        for func in list(temp.values()):
            assert callable(func['exe']), 'The function is not callable'


def test_get_function_global(global_module_setup):
    for item in global_module_setup.objectives:
        print(item)
        temp = utils.get_functions(item)
        assert (len(temp) == 3)
        for func in list(temp.values()):
            assert callable(func['exe']), 'The function is not callable'


def test_get_function_multi(multi_station_setup):
    for item in multi_station_setup.objectives:
        print(item)
        temp = utils.get_functions(item)
        assert (len(temp) == 3)
        for func in list(temp.values()):
            assert callable(func['exe']), 'The function is not callable'


######################################################################
# Test compute_gof function

def test_compute_gof(config_setup):
    temp = utils.compute_gof(config_setup)
    assert (temp == [0.72450915761519752, 1.2196478869306084])


def test_compute_no_error(no_error_setup):
    temp = utils.compute_gof(no_error_setup)
    # lrmse return 0 for no difference between the series
    assert (temp[0] == [0])
    assert (np.isnan(temp[1]))


def test_compute_multi_station(multi_station_setup):
    temp = utils.compute_gof(multi_station_setup)
    # lrmse return 0 for no difference between the series
    assert (pytest.approx(temp[0], 0.001) == 0.7245091)
    assert (pytest.approx(temp[1], 0.001) == -109.1739)


######################################################################
# Writing parameter files ...

def test_write_para(read_para_example, config_setup):
    # write the parameters to a file
    config_setup.para_names = read_para_example['names']
    para_values = read_para_example['values']
    utils.write_parameter_file(para_values, config_setup)
    # concat the strings and compare the files
    para_file = config_setup.pp + '/' + config_setup.parameter_file
    compare = filecmp.cmp(para_file,
                          './borg_hydro/swimpy/tests/test_input/subcatch.prm')
    assert (compare), 'Files do not match'


# Writing parameter files with multiple regions

def test_write_para_multi_region_a(read_para_example, config_mo_setup):
    # write the parameters to a file
    config_mo_setup.para_names = read_para_example['names']
    para_values = read_para_example['values']
    utils.write_parameter_file(para_values, config_mo_setup)
    # concat the strings and compare the files
    para_file = config_mo_setup.pp + '/' + config_mo_setup.parameter_file
    compare = filecmp.cmp(para_file,
                          './borg_hydro/swimpy/tests/test_input/subcatch_2.prm')
    assert (compare), 'Files do not match'


def test_write_para_multi_region_b(read_para_example, multi_station_setup):
    # write the parameters to a file
    multi_station_setup.para_names = read_para_example['names']
    para_values = read_para_example['values']
    utils.write_parameter_file(para_values, multi_station_setup)
    # concat the strings and compare the files
    para_file = multi_station_setup.pp + '/' + multi_station_setup.parameter_file
    compare = filecmp.cmp(para_file,
                          './borg_hydro/swimpy/tests/test_input/subcatch_4.prm')
    assert (compare), 'Files do not match'


######################################################################
# Test the window_ts function that cuts a dataframe to start and end dates

def test_window_ts(sim_simple):
    todays_date = datetime.datetime.now().date()
    start_date = todays_date + datetime.timedelta(days=1)
    end_date = todays_date + datetime.timedelta(days=4)
    temp = utils.window_ts(sim_simple, start_date=start_date,
                           end_date=end_date)
    assert(len(temp) == 3)


def test_window_ts_no_overlap(no_error_setup):
    no_error_setup.end = '1990-01-11'
    temp = utils.compute_gof(no_error_setup)
    assert (np.isnan(temp[1]))


def test_check_window_dates_format_start_date(sim_simple):
    with pytest.raises(Exception):
        utils.convert_dates(sim_simple, start_date=4)


def test_check_window_dates_format_end_date(sim_simple):
    with pytest.raises(Exception):
        utils.convert_dates(sim_simple, end_date=4)


def test_check_window_dates_equal_nothing(sim_simple):
    temp = utils.window_ts(sim_simple)
    assert (pd.DataFrame.equals(temp, sim_simple))


def test_check_window_dates_equal_string(sim_simple):
    todays_date = datetime.datetime.now().date()
    start_date = str(todays_date + datetime.timedelta(days=2))
    end_date = str(todays_date + datetime.timedelta(days=2))
    with pytest.raises(SystemExit):
        utils.window_ts(sim_simple, start_date, end_date)


def test_check_window_dates_smaller_end_date(sim_simple):
    todays_date = datetime.datetime.now().date()
    start_date = str(todays_date + datetime.timedelta(days=4))
    end_date = str(todays_date + datetime.timedelta(days=2))
    with pytest.raises(SystemExit):
        utils.window_ts(sim_simple, start_date, end_date)
