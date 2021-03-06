#!/usr/bin/python
'''
Tests for the swim_setup class.
'''
#
######################################################################

#       Filename: test_config.py

#       Author: Stefan Luedtke

######################################################################

from borg_hydro.swimpy import config
import pytest

######################################################################


# Class tests ...
def test_config_class(config_dict):
    '''test the class of the configuration objects '''
    assert isinstance(config_dict["config_01"], config.swim_setup)
    assert isinstance(config_dict["config_02"], config.swim_setup)
    assert isinstance(config_dict["config_03"], config.swim_setup)
    assert isinstance(config_dict["config_04"], config.swim_setup)
    assert isinstance(config_dict["config_06"], config.swim_setup)
    assert isinstance(config_dict["config_07"], config.swim_setup)
    assert isinstance(config_dict["config_08"], config.swim_setup)
    assert isinstance(config_dict["config_09"], config.swim_setup)
    assert isinstance(config_dict["config_10"], config.swim_setup)


def test_read_false_parameter_names():
    '''We use wrong parameter names here, so the initialization fails'''
    config_file = './borg_hydro/swimpy/tests/test_configs/05-config.json'
    with pytest.raises(KeyError):
        config.swim_setup(config_file)


######################################################################
# Test whether we get the correct number of objectives and parameters
def test_number_of_objectives(config_dict):
    '''test '''
    assert len(config_dict["config_01"].objectives) == 2
    assert len(config_dict["config_02"].objectives) == 4
    assert len(config_dict["config_03"].objectives) == 2
    assert len(config_dict["config_04"].objectives) == 3
    assert len(config_dict["config_06"].objectives) == 2
    assert len(config_dict["config_07"].objectives) == 4
    assert len(config_dict["config_08"].objectives) == 1
    assert len(config_dict["config_09"].objectives) == 1
    assert len(config_dict["config_10"].objectives) == 4


def test_number_of_epsilons(config_dict):
    '''test '''
    assert len(config_dict["config_01"].epsilons) == 2
    assert len(config_dict["config_02"].epsilons) == 4
    assert len(config_dict["config_03"].epsilons) == 2
    assert len(config_dict["config_04"].epsilons) == 3
    assert len(config_dict["config_06"].epsilons) == 2
    assert len(config_dict["config_07"].epsilons) == 4
    assert len(config_dict["config_08"].epsilons) == 1
    assert len(config_dict["config_09"].epsilons) == 1
    assert len(config_dict["config_10"].epsilons) == 4


def test_number_of_parameter_names(config_dict):
    '''test '''
    assert len(config_dict["config_01"].para_names) == 6
    assert len(config_dict["config_02"].para_names) == 2
    assert len(config_dict["config_03"].para_names) == 1
    assert len(config_dict["config_04"].para_names) == 1
    assert len(config_dict["config_06"].para_names) == 24
    assert len(config_dict["config_07"].para_names) == 24
    assert len(config_dict["config_08"].para_names) == 1
    assert len(config_dict["config_09"].para_names) == 6
    assert len(config_dict["config_10"].para_names) == 24


def test_number_of_parameter_limits(config_dict):
    '''test '''
    assert len(config_dict["config_01"].para_limits) == 6
    assert len(config_dict["config_02"].para_limits) == 2
    assert len(config_dict["config_03"].para_limits) == 1
    assert len(config_dict["config_04"].para_limits) == 1
    assert len(config_dict["config_06"].para_limits) == 24
    assert len(config_dict["config_07"].para_limits) == 24
    assert len(config_dict["config_08"].para_limits) == 1
    assert len(config_dict["config_09"].para_limits) == 6
    assert len(config_dict["config_10"].para_limits) == 24


def test_parse_parameter_limits(config_dict):
    '''Individual tests whether we got the correct parameter limits '''
    assert (config_dict['config_02'].para_limits ==
            [[0.00001, 3], [0.00001, 3]])

    assert (config_dict['config_06'].para_limits ==
            [[0.00001, 3], [0.1, 1.2], [0.00001, 2],
             [1, 60], [0.1, 200], [0.1, 4]] * 4)

    assert (config_dict['config_09'].para_limits ==
            [[0.00001, 3], [0.1, 1.2]] * 3)


def test_split_nested_objectives(config_dict):
    '''Check the names from the nested configurations '''
    # Test case 04
    temp_04 = config_dict['config_04']
    assert (temp_04.objectives[0]['pattern'] == "50201"),\
        'Objectives not correctly parsed'
    assert (temp_04.objectives[1]['pattern'] == "50208"),\
        'Objectives not correctly parsed'
    assert (temp_04.objectives[2]['pattern'] == "40208"),\
        'Objectives not correctly parsed'
    # Test case 07
    temp_07 = config_dict['config_07']
    assert (temp_07.objectives[0]['pattern'] == "50201"),\
        'Objectives not correctly parsed'
    assert (temp_07.objectives[1]['pattern'] == "50208"),\
        'Objectives not correctly parsed'
    assert (temp_07.objectives[2]['pattern'] == "50201"),\
        'Objectives not correctly parsed'
    assert (temp_07.objectives[3]['pattern'] == "50208"),\
        'Objectives not correctly parsed'
    # Test case 10
    temp_10 = config_dict['config_10']
    assert (temp_10.objectives[0]['pattern'] == "50208"),\
        'Objectives not correctly parsed'
    assert (temp_10.objectives[1]['pattern'] == "50208"),\
        'Objectives not correctly parsed'
    assert (temp_10.objectives[2]['pattern'] == "50201"),\
        'Objectives not correctly parsed'
    assert (temp_10.objectives[3]['pattern'] == "50201"),\
        'Objectives not correctly parsed'


def test_parse_aggregation_level(config_dict):
    '''Check whether the aggregation is parsed correctly'''
    # Test case 04
    temp_04 = config_dict['config_04']
    # Test case 10
    temp_10 = config_dict['config_10']
    # No aggregation level given
    with pytest.raises(KeyError):
        temp_04.objectives[0]['aggregation']
        temp_04.objectives[1]['aggregation']
        temp_04.objectives[2]['aggregation']
        temp_10.objectives[0]['aggregation']
        temp_10.objectives[2]['aggregation']
    # with aggregation level given
    assert (temp_10.objectives[1]['aggregation']['period'] == "W"),\
        'Aggregation level not correctly parsed'
    assert (temp_10.objectives[1]['aggregation']['function'] == "mean"),\
        'Aggregation level not correctly parsed'
    assert (temp_10.objectives[3]['aggregation']['period'] == "M"),\
        'Aggregation level not correctly parsed'
    assert (temp_10.objectives[3]['aggregation']['function'] == "sum"),\
        'Aggregation level not correctly parsed'
