#!/usr/bin/python
# show commands being executed, per debug
#
######################################################################

#       Filename: test_config.py

#       Author: Stefan Luedtke

######################################################################

from borg_hydro.swimpy import config
import pytest

######################################################################


# Class tests ...
def test_read_config(config_setup):
    '''test '''
    assert isinstance(config_setup, config.swim_setup), 'Wrong data type'


def test_read_config_mo(config_mo_setup):
    '''test '''
    assert isinstance(config_mo_setup, config.swim_setup), 'Wrong data type'


def test_config_global_module(global_module_setup):
    '''test '''
    assert isinstance(global_module_setup, config.swim_setup),\
        'Wrong data type'


def test_read_multi_station(multi_station_setup):
    '''test '''
    assert isinstance(multi_station_setup, config.swim_setup),\
        'Wrong data type'


def test_read_multi_nested_station(multi_station_nested_setup):
    '''test '''
    assert isinstance(multi_station_nested_setup, config.swim_setup),\
        'Wrong data type'


def test_read_no_error(no_error_setup):
    '''test '''
    assert isinstance(no_error_setup, config.swim_setup),\
        'Wrong data type'


def test_read_no_error_nested(no_error_nested_setup):
    '''test '''
    assert isinstance(no_error_nested_setup, config.swim_setup),\
        'Wrong data type'


def test_read_false_parameter():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_configs/05-config.json'
    with pytest.raises(KeyError):
        config.swim_setup(config_file)


######################################################################
# Test whether we get the correct number of objectives and parameters
def test_parse_parameter_names(config_mo_setup, config_setup,
                               global_module_setup, multi_station_setup,
                               para_region_setup):
    '''test '''
    assert (len(config_mo_setup.para_names) == 2),\
        'Wrong number of parameter names'
    assert (len(config_setup.para_names) == 6),\
        'Wrong number of parameter names'
    assert (len(global_module_setup.para_names) == 1),\
        'Wrong number of parameter names'
    assert (len(multi_station_setup.para_names) == 24),\
        'Wrong number of parameter names'
    assert (len(para_region_setup.para_names) == 6),\
        'Wrong number of parameter names'


def test_parse_parameter_range(config_mo_setup, config_setup,
                               global_module_setup, multi_station_setup,
                               para_region_setup):
    '''test '''
    assert (len(config_mo_setup.para_limits) == 2),\
        'Wrong number in parameter range'
    assert (len(config_setup.para_limits) == 6),\
        'Wrong number in parameter range'
    assert (len(global_module_setup.para_limits) == 1),\
        'Wrong number in parameter range'
    assert (len(multi_station_setup.para_limits) == 24),\
        'Wrong number in parameter range'
    assert (len(para_region_setup.para_limits) == 6),\
        'Wrong number in parameter range'


def test_parse_parameter_values_mo(config_mo_setup):
    '''test '''
    assert (config_mo_setup.para_limits == [[0.00001, 3], [0.00001, 3]])


def test_parse_parameter_values_multi(multi_station_setup):
    # test the mmulti station setup
    multi_station_para_hard_coded = [[0.00001, 3], [0.1, 1.2], [0.00001, 2],
                                     [1, 60], [0.1, 200], [0.1, 4]] * 4
    assert (multi_station_setup.para_limits == multi_station_para_hard_coded),\
        'Parameters do not match'


def test_parse_parameter_values_para_region_setup(para_region_setup):
    # test the mmulti station setup
    multi_station_para_hard_coded = [[0.00001, 3], [0.1, 1.2]] * 3
    assert (para_region_setup.para_limits == multi_station_para_hard_coded),\
        'Parameters do not match'


def test_parse_objectives(config_mo_setup, config_setup, global_module_setup,
                          multi_station_setup, para_region_setup,
                          no_error_nested_setup, multi_station_nested_setup):
    '''test '''
    assert (len(config_mo_setup.objectives) == 4),\
        'Wrong number of objectives'
    assert (len(config_setup.objectives) == 2),\
        'Wrong number of objectives'
    assert (len(global_module_setup.objectives) == 1),\
        'Wrong number of objectives'
    assert (len(multi_station_setup.objectives) == 2),\
        'Wrong number of objectives'
    assert (len(para_region_setup.objectives) == 1),\
        'Wrong number of objectives'
    assert (len(no_error_nested_setup.objectives) == 3),\
        'Wrong number of objectives'
    assert (len(no_error_nested_setup.objectives) == 3),\
        'Wrong number of objectives'
    assert (len(multi_station_nested_setup.objectives) == 4),\
        'Wrong number of objectives'


def test_parse_epsilons(config_mo_setup, config_setup, global_module_setup,
                        multi_station_setup, para_region_setup,
                        no_error_nested_setup, multi_station_nested_setup):
    '''test '''
    assert (len(config_mo_setup.epsilons) == 4),\
        'Wrong number of epsilons'
    assert (len(config_setup.epsilons) == 2),\
        'Wrong number of epsilons'
    assert (len(global_module_setup.epsilons) == 1),\
        'Wrong number of epsilons'
    assert (len(multi_station_setup.epsilons) == 2),\
        'Wrong number of epsilons'
    assert (len(para_region_setup.epsilons) == 1),\
        'Wrong number of epsilons'
    assert (len(no_error_nested_setup.epsilons) == 3),\
        'Wrong number of epsilons'
    assert (len(multi_station_nested_setup.epsilons) == 4),\
        'Wrong number of epsilons'


def test_split_nested_objectives(no_error_nested_setup,
                                 multi_station_nested_setup):
    '''test '''
    assert (no_error_nested_setup.objectives[0]['pattern'] == "50201"),\
        'Objectives not correctly parsed'
    assert (no_error_nested_setup.objectives[1]['pattern'] == "50208"),\
        'Objectives not correctly parsed'
    assert (no_error_nested_setup.objectives[2]['pattern'] == "40208"),\
        'Objectives not correctly parsed'

    assert (multi_station_nested_setup.objectives[0]['pattern'] == "50201"),\
        'Objectives not correctly parsed'
    assert (multi_station_nested_setup.objectives[1]['pattern'] == "50208"),\
        'Objectives not correctly parsed'
    assert (multi_station_nested_setup.objectives[2]['pattern'] == "50201"),\
        'Objectives not correctly parsed'
    assert (multi_station_nested_setup.objectives[3]['pattern'] == "50208"),\
        'Objectives not correctly parsed'

def test_epsilons_values_para_region_setup(para_region_setup):
    ''' test the mmulti station setup'''
    assert para_region_setup.epsilons == [0.2],\
        'Parameters do not match'
