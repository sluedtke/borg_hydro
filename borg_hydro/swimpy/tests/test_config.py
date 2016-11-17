#!/usr/bin/python
# show commands being executed, per debug
#
######################################################################

#       Filename: test_config.py

#       Author: Stefan Luedtke

######################################################################

from borg_hydro.swimpy import config


######################################################################


# Class tests ...
def test_read_config(config_setup, config_para, config_obj):
    '''test '''
    assert isinstance(config_setup, config.swim_setup), 'Wrong data type'
    assert isinstance(config_para, config.swim_parameter), 'Wrong data type'
    assert isinstance(config_obj, config.swim_objectives), 'Wrong data type'


def test_read_config_mo(config_mo_setup, config_mo_para, config_mo_obj):
    '''test '''
    assert isinstance(config_mo_setup, config.swim_setup), 'Wrong data type'
    assert isinstance(config_mo_para, config.swim_parameter), 'Wrong data type'
    assert isinstance(config_mo_obj, config.swim_objectives), 'Wrong data type'


def test_config_global_module(global_module_setup, global_module_para,
                              global_module_obj):
    '''test '''
    assert isinstance(global_module_setup, config.swim_setup),\
        'Wrong data type'
    assert isinstance(global_module_para, config.swim_parameter),\
        'Wrong data type'
    assert isinstance(global_module_obj, config.swim_objectives),\
        'Wrong data type'


def test_read_multi_station(multi_station_setup, multi_station_para,
                            multi_station_obj):
    '''test '''
    assert isinstance(multi_station_setup, config.swim_setup),\
        'Wrong data type'
    assert isinstance(multi_station_para, config.swim_parameter),\
        'Wrong data type'
    assert isinstance(multi_station_obj, config.swim_objectives),\
        'Wrong data type'


def test_read_no_error(no_error_setup, no_error_para, no_error_obj):
    '''test '''
    assert isinstance(no_error_setup, config.swim_setup),\
        'Wrong data type'
    assert isinstance(no_error_para, config.swim_parameter),\
        'Wrong data type'
    assert isinstance(no_error_obj, config.swim_objectives),\
        'Wrong data type'


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
