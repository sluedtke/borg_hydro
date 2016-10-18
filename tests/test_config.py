#!/usr/bin/python
# show commands being executed, per debug
#
######################################################################

#       Filename: test_config.py

#       Author: Stefan Luedtke

######################################################################

from swimpy import config


######################################################################


# Class tests ...
def test_read_config():
    '''test '''
    config_file = './tests/test_data_config/config.json'
    temp = config.swim_setup(config_file)
    assert isinstance(temp, config.swim_setup), 'Wrong data type'
    temp = config.swim_parameter(config_file)
    assert isinstance(temp, config.swim_parameter), 'Wrong data type'
    temp = config.swim_objectives(config_file)
    assert isinstance(temp, config.swim_objectives), 'Wrong data type'


def test_read_config_mo():
    '''test '''
    config_file = './tests/test_data_config/config_mo.json'
    temp = config.swim_setup(config_file)
    assert isinstance(temp, config.swim_setup), 'Wrong data type'
    temp = config.swim_parameter(config_file)
    assert isinstance(temp, config.swim_parameter), 'Wrong data type'
    temp = config.swim_objectives(config_file)
    assert isinstance(temp, config.swim_objectives), 'Wrong data type'


def test_config_global_module():
    '''test '''
    config_file = './tests/test_data_config/global_module.json'
    temp = config.swim_setup(config_file)
    temp = config.swim_parameter(config_file)
    assert isinstance(temp, config.swim_parameter), 'Wrong data type'
    temp = config.swim_objectives(config_file)
    assert isinstance(temp, config.swim_objectives), 'Wrong data type'


def test_read_multi_station():
    '''test '''
    config_file = './tests/test_data_config/multi_station.json'
    temp = config.swim_setup(config_file)
    temp = config.swim_parameter(config_file)
    assert isinstance(temp, config.swim_parameter), 'Wrong data type'
    temp = config.swim_objectives(config_file)
    assert isinstance(temp, config.swim_objectives), 'Wrong data type'


######################################################################
# Test whether we get the correct number of objectives and parameters
def test_parse_parameter_names(config_mo_para, config_para,
                               global_module_para):
    '''test '''
    assert (len(config_mo_para.para_names) == 1),\
            'Wrong number of parameter names'
    assert (len(config_para.para_names) == 6),\
            'Wrong number of parameter names'
    assert (len(global_module_para.para_names) == 1),\
            'Wrong number of parameter names'


def test_parse_parameter_range(config_mo_para, config_para, global_module_para):
    '''test '''
    assert (len(config_mo_para.para_range) == 1),\
            'Wrong number in parameter range'
    assert (len(config_para.para_range) == 6),\
            'Wrong number in parameter range'
    assert (len(global_module_para.para_range) == 1),\
            'Wrong number in parameter range'


def test_parse_objectives(config_mo_obj, config_obj, global_module_obj):
    '''test '''
    assert (len(config_mo_obj.objectives) == 4),\
            'Wrong number of objectives'
    assert (len(config_obj.objectives) == 2),\
            'Wrong number of objectives'
    assert (len(global_module_obj.objectives) == 1),\
            'Wrong number of objectives'
