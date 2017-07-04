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

# That one fails, but only for the second item, the first itmen has an star date 
# for the observation date and since we use only values existent at both time 
# series, the new start data does not matter
@pytest.mark.xfail
def test_compute_gof_fail(config_setup):
    temp = utils.compute_gof(config_setup)
    assert (temp == [[0.72450915761519752], [1.2196478869306084]])


def test_compute_gof(config_setup):
    # overwrite the start date from the configuration file
    config_setup.start = '1990-01-01'
    temp = utils.compute_gof(config_setup)
    assert (temp == [[0.72450915761519752], [1.2196478869306084]])


def test_compute_gof_mo_modify_start(config_mo_setup):
    # overwrite the start date from the configuration file
    config_mo_setup.start = '1990-01-11'
    temp = utils.compute_gof(config_mo_setup)
    assert (pytest.approx(temp[0], 0.001) == [0.7343])
    assert (pytest.approx(temp[1], 0.001) == [1.1576])


def test_compute_gof_mo_modify_end(config_mo_setup):
    # overwrite the start date from the configuration file
    config_mo_setup.end = '1990-01-09'
    temp = utils.compute_gof(config_mo_setup)
    assert (pytest.approx(temp[0], 0.001) == [0.7052])
    assert (pytest.approx(temp[1], 0.001) == [1.246])


def test_compute_gof_mo(config_mo_setup):
    temp = utils.compute_gof(config_mo_setup)
    assert (pytest.approx(temp[0], 0.001) == [0.7245])
    assert (pytest.approx(temp[1], 0.001) == [1.2196])
    assert (pytest.approx(temp[2], 0.001) == [1.6799])
    assert (pytest.approx(temp[3], 0.001) == [13.17])


def test_compute_no_error(no_error_setup):
    temp = utils.compute_gof(no_error_setup)
    # lrmse return 0 for no difference between the series
    assert (temp[0] == [0.0, 0.0, 0.0])
    assert (np.isnan(temp[1]))


def test_compute_multi_station(multi_station_setup):
    temp = utils.compute_gof(multi_station_setup)
    # lrmse return 0 for no difference between the series
    assert (pytest.approx(temp[0], 0.001) == [0.7245091576151975, 0.7254229337221346])
    assert (pytest.approx(temp[1], 0.001) == [-109.64159579355754, -108.70622740963847])


######################################################################
# Writing parameter files ...
def create_random_draw(swim_config):
    '''
    Draws a set of random numbers according to the parameter settings and
    parameter regions given in the swim class.
    '''
    random_draw = np.random.uniform(list(zip(*swim_config.para_limits))[0],
                                    list(zip(*swim_config.para_limits))[1],
                                    len(swim_config.para_limits)).tolist()
    return(random_draw)


def write_parameter_template(swim_config):
    '''
    This function simply writes the parameter template of the swim config to a
    file.
    '''
    para_file = swim_config.pp + '/' + swim_config.parameter_file
    swim_config.para_template.to_csv(para_file, sep='\t', encoding='utf-8',
                                     header=True, index=True)


# -----------------------------------
def test_write_para_template(config_setup):
    # write the parameters to a file
    write_parameter_template(config_setup)
    # concat the strings and compare the files
    para_file = config_setup.pp + '/' + config_setup.parameter_file
    compare = filecmp.cmp(para_file,
                          './borg_hydro/swimpy/tests/test_input/subcatch.prm')
    assert (compare), 'Files do not match'


# Writing parameter files with multiple regions
def test_write_para_template_multi_region_a(config_mo_setup):
    # write the parameters to a file
    write_parameter_template(config_mo_setup)
    # concat the strings and compare the files
    para_file = config_mo_setup.pp + '/' + config_mo_setup.parameter_file
    compare = filecmp.cmp(para_file,
                          './borg_hydro/swimpy/tests/test_input/subcatch_2.prm')
    assert (compare), 'Files do not match'


def test_write_para_template_multi_region_b(multi_station_setup):
    # write the parameters to a file
    write_parameter_template(multi_station_setup)
    # concat the strings and compare the files
    para_file = multi_station_setup.pp + '/' +\
        multi_station_setup.parameter_file
    compare = filecmp.cmp(para_file,
                          './borg_hydro/swimpy/tests/test_input/subcatch_4.prm')
    assert (compare), 'Files do not match'


# -----------------------------------
@pytest.mark.xfail
def test_create_para_borg_false_b(config_setup):
    rdn_draw = create_random_draw(config_setup)
    # create a random parameter set that is used to update the template
    temp_para_borg = utils.create_para_borg(config_setup, rdn_draw)
    pd.util.testing.assert_frame_equal(temp_para_borg,
                                       config_setup.para_template)


@pytest.mark.xfail
def test_create_para_borg_false(config_mo_setup):
    # create a random parameter set that is used to update the template
    rdn_draw = create_random_draw(config_mo_setup)
    temp_para_borg = utils.create_para_borg(config_mo_setup, rdn_draw)
    pd.util.testing.assert_frame_equal(temp_para_borg,
                                       config_mo_setup.para_template)


@pytest.mark.xfail
def test_create_para_borg_false_a(multi_station_setup):
    # create a random parameter set that is used to update the template
    rdn_draw = create_random_draw(multi_station_setup)
    temp_para_borg = utils.create_para_borg(multi_station_setup, rdn_draw)
    pd.util.testing.assert_frame_equal(temp_para_borg,
                                       multi_station_setup.para_template)


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
    no_error_setup.end = '1990-01-05'
    with pytest.raises(SystemExit):
        temp = utils.compute_gof(no_error_setup)


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
