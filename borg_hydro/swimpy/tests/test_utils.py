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

def test_get_function(config_01):
    for item in config_01.objectives:
        temp = utils.get_functions(item)
        assert (len(temp) == 3)
        for func in list(temp.values()):
            assert callable(func['exe']), 'The function is not callable'


def test_get_function_mo(config_02):
    for item in config_02.objectives:
        temp = utils.get_functions(item)
        assert (len(temp) == 3)
        for func in list(temp.values()):
            assert callable(func['exe']), 'The function is not callable'


def test_get_function_global(config_08):
    for item in config_08.objectives:
        print(item)
        temp = utils.get_functions(item)
        assert (len(temp) == 3)
        for func in list(temp.values()):
            assert callable(func['exe']), 'The function is not callable'


def test_get_function_multi(config_06):
    for item in config_06.objectives:
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
def test_compute_gof_fail(config_01):
    temp = utils.compute_gof(config_01)
    assert (temp == [[0.72450915761519752], [1.2196478869306084]])


def test_compute_gof(config_01):
    # overwrite the start date from the configuration file
    config_01.evp['start_date'] = '1990-01-01'
    temp = utils.compute_gof(config_01)
    assert (temp == [[0.72450915761519752], [1.2196478869306084]])


def test_compute_gof_mo_modify_start(config_02):
    # overwrite the start date from the configuration file
    config_02.evp['start_date'] = '1990-01-11'
    temp = utils.compute_gof(config_02)
    assert (pytest.approx(temp[0], 0.001) == [0.7343])
    assert (pytest.approx(temp[1], 0.001) == [1.1576])


def test_compute_gof_mo_modify_end(config_02):
    # overwrite the start date from the configuration file
    config_02.evp['end_date'] = '1990-01-09'
    temp = utils.compute_gof(config_02)
    assert (pytest.approx(temp[0], 0.001) == [0.7052])
    assert (pytest.approx(temp[1], 0.001) == [1.246])


def test_compute_gof_mo(config_02):
    temp = utils.compute_gof(config_02)
    assert (pytest.approx(temp[0], 0.001) == [0.7245])
    assert (pytest.approx(temp[1], 0.001) == [1.2196])
    assert (pytest.approx(temp[2], 0.001) == [1.6799])
    assert (pytest.approx(temp[3], 0.001) == [13.17])


def test_compute_no_error(config_03):
    temp = utils.compute_gof(config_03)
    # lrmse return 0 for no difference between the series
    assert (temp[0] == [0.0, 0.0, 0.0])
    assert (np.isnan(temp[1]))


def test_compute_no_error_nested(config_04):
    temp = utils.compute_gof(config_04)
    # lrmse return 0 for no difference between the series
    assert (temp[0] == [0.0])
    assert (temp[1] == [0.0])
    assert (temp[2] == [0.0])


def test_compute_multi_station(config_06):
    temp = utils.compute_gof(config_06)
    # lrmse return 0 for no difference between the series
    assert (pytest.approx(temp[0], 0.001) == [0.72450915761, 0.72542293372])
    assert (pytest.approx(temp[1], 0.001) == [-109.64159579, -108.70622740])


def test_compute_multi_station_nested(config_dict):
    temp = utils.compute_gof(config_dict['config_07'])
    # lrmse return 0 for no difference between the series
    assert (pytest.approx(temp[0], 0.001) == [0.72450915761])
    assert (pytest.approx(temp[1], 0.001) == [0.72542293372])
    assert (pytest.approx(temp[2], 0.001) == [-109.64159579])
    assert (pytest.approx(temp[3], 0.001) == [-108.70622740])


def test_compute_multi_station_aggregation(config_dict):
    # test the aggregation results
    temp = utils.compute_gof(config_dict['config_10'])
    # lrmse return 0 for no difference between the series
    assert (pytest.approx(temp[0], 0.001) == [69.3])
    assert (pytest.approx(temp[1], 0.001) == [-15.027036744])
    assert (pytest.approx(temp[2], 0.001) == [115.5])
    assert (pytest.approx(temp[3], 0.001) == [-14.069738052])


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


# -----------------------------------
def test_write_para_template(config_01, tmpdir):
    # create a temporary dir to write into
    p = str(tmpdir.mkdir("test_input").join("para.prm"))
    config_01.parameter_file = p
    # write the parameters to a file
    utils.write_parameter_file(config_01, config_01.para_template)
    # concat the strings and compare the files
    compare = filecmp.cmp(config_01.parameter_file,
                          './borg_hydro/swimpy/tests/test_input/subcatch.prm')
    assert (compare), 'Files do not match'


# Writing parameter files with multiple regions
def test_write_para_template_multi_region_a(config_02, tmpdir):
    p = str(tmpdir.mkdir("test_input").join("para.prm"))
    config_02.parameter_file = p
    # write the parameters to a file
    utils.write_parameter_file(config_02, config_02.para_template)
    # concat the strings and compare the files
    compare = filecmp.cmp(config_02.parameter_file,
                          './borg_hydro/swimpy/tests/test_input/subcatch_2.prm')
    assert (compare), 'Files do not match'


def test_write_para_template_multi_region_b(config_06, tmpdir):
    p = str(tmpdir.mkdir("test_input").join("para.prm"))
    config_06.parameter_file = p
    # write the parameters to a file
    utils.write_parameter_file(config_06, config_06.para_template)
    # concat the strings and compare the files
    compare = filecmp.cmp(config_06.parameter_file,
                          './borg_hydro/swimpy/tests/test_input/subcatch_4.prm')
    assert (compare), 'Files do not match'


def test_write_para_template_para_region(config_09, tmpdir):
    p = str(tmpdir.mkdir("test_input").join("para.prm"))
    config_09.parameter_file = p
    # write the parameters to a file
    # import pdb; pdb.set_trace()
    utils.write_parameter_file(config_09, config_09.para_template)
    # concat the strings and compare the files
    compare = filecmp.cmp(config_09.parameter_file,
                          './borg_hydro/swimpy/tests/test_input/subcatch_5.prm')
    assert (compare), 'Files do not match'


# -----------------------------------
@pytest.mark.xfail
def test_create_para_borg_false_b(config_01):
    rdn_draw = create_random_draw(config_01)
    # create a random parameter set that is used to update the template
    temp_para_borg = utils.create_para_borg(config_01, rdn_draw)
    pd.util.testing.assert_frame_equal(temp_para_borg,
                                       config_01.para_template)


@pytest.mark.xfail
def test_create_para_borg_false(config_02):
    # create a random parameter set that is used to update the template
    rdn_draw = create_random_draw(config_02)
    temp_para_borg = utils.create_para_borg(config_02, rdn_draw)
    pd.util.testing.assert_frame_equal(temp_para_borg,
                                       config_02.para_template)


@pytest.mark.xfail
def test_create_para_borg_false_a(config_06):
    # create a random parameter set that is used to update the template
    rdn_draw = create_random_draw(config_06)
    temp_para_borg = utils.create_para_borg(config_06, rdn_draw)
    pd.util.testing.assert_frame_equal(temp_para_borg,
                                       config_06.para_template)


@pytest.mark.xfail
def test_create_para_borg_config_09_fail(config_09):
    # create a random parameter set that is used to update the template
    rdn_draw = create_random_draw(config_09)
    temp_para_borg = utils.create_para_borg(config_09, rdn_draw)
    pd.util.testing.assert_frame_equal(temp_para_borg,
                                       config_09.para_template)


# The following two tests (a and b) show that the selective parameter regions
# work in both cases:
# a: if we select only the rows that were not chosen by the config
def test_create_para_borg_config_09_a(config_09):
    # create a random parameter set that is used to update the template
    rdn_draw = create_random_draw(config_09)
    para_borg = utils.create_para_borg(config_09, rdn_draw)
    # get the list of catchmentIDs we changed
    catch_ids = config_09.para_preg_ids
    # subset to the rows we did __NOT__ changed
    para_borg_true = para_borg.loc[~para_borg.index.isin(catch_ids)]
    # subset to the rows we did __NOT__ changed
    para_template = config_09.para_template
    para_template_true = para_template[~para_template.index.isin(catch_ids)]
    # assert for equality
    pd.util.testing.assert_frame_equal(para_borg_true, para_template_true)


# b: if we select only the columns that were not chosen
def test_create_para_borg_config_09_b(config_09):
    # create a random parameter set that is used to update the template
    rdn_draw = create_random_draw(config_09)
    para_borg = utils.create_para_borg(config_09, rdn_draw)
    # get the list of parameters we are working on
    para_names = list(set(config_09.para_names))
    # subset to the column we did __NOT__ changed
    para_borg.drop(para_names, axis = 1, inplace = True)
    # subset to the rows we did __NOT__ changed
    para_template = config_09.para_template
    para_template.drop(para_names, axis = 1, inplace = True)
    # assert for equality
    pd.util.testing.assert_frame_equal(para_borg, para_template)


######################################################################
# Test the function to convert strings given a specific format
def test_check_convert_dates():
    # no Exceptiosn
    # daily values
    utils.convert_dates(date_var='2001-10-30')
    utils.convert_dates(date_var='2001-10-30', d_format='%Y-%m-%d')
    utils.convert_dates(date_var='2001-30-10', d_format='%Y-%d-%m')
    utils.convert_dates(date_var='2001-30-oct', d_format='%Y-%d-%b')
    utils.convert_dates(date_var='2001-oct-30', d_format='%Y-%b-%d')
    # monthly
    utils.convert_dates(date_var='2001-10', d_format='%Y-%m')
    utils.convert_dates(date_var='2001-oct', d_format='%Y-%b')
    utils.convert_dates(date_var='2001-October', d_format='%Y-%B')
    # julian day
    utils.convert_dates(date_var='2001-200', d_format='%Y-%j')
    # throws an exception
    with pytest.raises(Exception):
        # nonsense
        utils.convert_dates("lkdfsjklfj")
        utils.convert_dates(date_var='2001-400', d_format='%Y-%j')
        utils.convert_dates(date_var='2001-month', d_format='%Y-%b')


######################################################################
# Test the window_ts function that cuts a dataframe to start and end dates
def test_window_ts(sim_simple):
    todays_date = datetime.datetime.now().date()
    start_date = todays_date + datetime.timedelta(days=1)
    end_date = todays_date + datetime.timedelta(days=4)
    temp = utils.window_ts(sim_simple, start_date=start_date,
                           end_date=end_date)
    assert(len(temp) == 3)


def test_window_ts_no_overlap(config_03):
    config_03.evp['end_date'] = '1990-01-05'
    with pytest.raises(SystemExit):
        utils.compute_gof(config_03)


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
