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
def test_read_config(config_01):
    '''test '''
    assert isinstance(config_01, config.swim_setup), 'Wrong data type'


def test_read_config_mo(config_02):
    '''test '''
    assert isinstance(config_02, config.swim_setup), 'Wrong data type'


def test_config_global_module(config_08):
    '''test '''
    assert isinstance(config_08, config.swim_setup),\
        'Wrong data type'


def test_read_multi_station(config_06):
    '''test '''
    assert isinstance(config_06, config.swim_setup),\
        'Wrong data type'


def test_read_multi_nested_station(config_07):
    '''test '''
    assert isinstance(config_07, config.swim_setup),\
        'Wrong data type'


def test_read_no_error(config_03):
    '''test '''
    assert isinstance(config_03, config.swim_setup),\
        'Wrong data type'


def test_read_no_error_nested(config_04):
    '''test '''
    assert isinstance(config_04, config.swim_setup),\
        'Wrong data type'


def test_read_false_parameter():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_configs/05-config.json'
    with pytest.raises(KeyError):
        config.swim_setup(config_file)


######################################################################
# Test whether we get the correct number of objectives and parameters
def test_parse_parameter_names(config_02, config_01,
                               config_08, config_06,
                               config_09):
    '''test '''
    assert (len(config_02.para_names) == 2),\
        'Wrong number of parameter names'
    assert (len(config_01.para_names) == 6),\
        'Wrong number of parameter names'
    assert (len(config_08.para_names) == 1),\
        'Wrong number of parameter names'
    assert (len(config_06.para_names) == 24),\
        'Wrong number of parameter names'
    assert (len(config_09.para_names) == 6),\
        'Wrong number of parameter names'


def test_parse_parameter_range(config_02, config_01,
                               config_08, config_06,
                               config_09):
    '''test '''
    assert (len(config_02.para_limits) == 2),\
        'Wrong number in parameter range'
    assert (len(config_01.para_limits) == 6),\
        'Wrong number in parameter range'
    assert (len(config_08.para_limits) == 1),\
        'Wrong number in parameter range'
    assert (len(config_06.para_limits) == 24),\
        'Wrong number in parameter range'
    assert (len(config_09.para_limits) == 6),\
        'Wrong number in parameter range'


def test_parse_parameter_values_mo(config_02):
    '''test '''
    assert (config_02.para_limits == [[0.00001, 3], [0.00001, 3]])


def test_parse_parameter_values_multi(config_06):
    # test the mmulti station setup
    multi_station_para_hard_coded = [[0.00001, 3], [0.1, 1.2], [0.00001, 2],
                                     [1, 60], [0.1, 200], [0.1, 4]] * 4
    assert (config_06.para_limits == multi_station_para_hard_coded),\
        'Parameters do not match'


def test_parse_parameter_values_config_09(config_09):
    # test the mmulti station setup
    multi_station_para_hard_coded = [[0.00001, 3], [0.1, 1.2]] * 3
    assert (config_09.para_limits == multi_station_para_hard_coded),\
        'Parameters do not match'


def test_parse_objectives(config_02, config_01, config_08,
                          config_06, config_09,
                          config_04, config_07):
    '''test '''
    assert (len(config_02.objectives) == 4),\
        'Wrong number of objectives'
    assert (len(config_01.objectives) == 2),\
        'Wrong number of objectives'
    assert (len(config_08.objectives) == 1),\
        'Wrong number of objectives'
    assert (len(config_06.objectives) == 2),\
        'Wrong number of objectives'
    assert (len(config_09.objectives) == 1),\
        'Wrong number of objectives'
    assert (len(config_04.objectives) == 3),\
        'Wrong number of objectives'
    assert (len(config_04.objectives) == 3),\
        'Wrong number of objectives'
    assert (len(config_07.objectives) == 4),\
        'Wrong number of objectives'


def test_parse_epsilons(config_02, config_01, config_08,
                        config_06, config_09,
                        config_04, config_07):
    '''test '''
    assert (len(config_02.epsilons) == 4),\
        'Wrong number of epsilons'
    assert (len(config_01.epsilons) == 2),\
        'Wrong number of epsilons'
    assert (len(config_08.epsilons) == 1),\
        'Wrong number of epsilons'
    assert (len(config_06.epsilons) == 2),\
        'Wrong number of epsilons'
    assert (len(config_09.epsilons) == 1),\
        'Wrong number of epsilons'
    assert (len(config_04.epsilons) == 3),\
        'Wrong number of epsilons'
    assert (len(config_07.epsilons) == 4),\
        'Wrong number of epsilons'


def test_split_nested_objectives(config_04,
                                 config_07):
    '''test '''
    assert (config_04.objectives[0]['pattern'] == "50201"),\
        'Objectives not correctly parsed'
    assert (config_04.objectives[1]['pattern'] == "50208"),\
        'Objectives not correctly parsed'
    assert (config_04.objectives[2]['pattern'] == "40208"),\
        'Objectives not correctly parsed'

    assert (config_07.objectives[0]['pattern'] == "50201"),\
        'Objectives not correctly parsed'
    assert (config_07.objectives[1]['pattern'] == "50208"),\
        'Objectives not correctly parsed'
    assert (config_07.objectives[2]['pattern'] == "50201"),\
        'Objectives not correctly parsed'
    assert (config_07.objectives[3]['pattern'] == "50208"),\
        'Objectives not correctly parsed'

def test_epsilons_values_config_09(config_09):
    ''' test the mmulti station setup'''
    assert config_09.epsilons == [0.2],\
        'Parameters do not match'
