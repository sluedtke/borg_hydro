#!/usr/bin/python
# show commands being executed, per debug
#
######################################################################

#       Filename: test_config.py

#       Author: Stefan Luedtke

######################################################################

import pytest
from swimpy import config, gof_python

######################################################################


def test_read_config():
    '''test '''
    config_file = './tests/test_data_config/config.json'
    temp = config.user_borg_model(config_file)
    assert isinstance(temp, config.user_borg_model), 'Wrong data type'


@pytest.fixture()
def config_data():
    '''test '''
    config_file = './tests/test_data_config/config.json'
    temp = config.user_borg_model(config_file)
    return(temp)


def test_read_config_mo():
    '''test '''
    config_file = './tests/test_data_config/config_mo.json'
    temp = config.user_borg_model(config_file)
    assert isinstance(temp, config.user_borg_model), 'Wrong data type'


@pytest.fixture()
def config_mo_data():
    '''test '''
    config_file = './tests/test_data_config/config_mo.json'
    temp = config.user_borg_model(config_file)
    return(temp)


def test_config_global_module():
    '''test '''
    config_file = './tests/test_data_config/global_module.json'
    temp = config.user_borg_model(config_file)
    return(temp)


@pytest.fixture()
def global_module_data():
    '''test '''
    config_file = './tests/test_data_config/global_module.json'
    temp = config.user_borg_model(config_file)
    return(temp)


def test_parse_objectives(config_mo_data, config_data, global_module_data):
    '''test '''
    assert (len(config_mo_data.objectives) == 4),\
            'Wrong number of objectives'
    assert (len(config_data.objectives) == 2),\
            'Wrong number of objectives'
    assert (len(global_module_data.objectives) == 1),\
            'Wrong number of objectives'


# test the get_functions function- that one is crucial and quite tricky because
# we try to catch module and function name depending on the scope.
def test_get_function(config_data):
    for item in config_data.objectives:
        temp = gof_python.get_functions(item)
        assert (len(temp) == 3)
        for func in list(temp.values()):
            assert callable(func), 'The function is not callable'


def test_get_function_mo(config_mo_data):
    for item in config_mo_data.objectives:
        temp = gof_python.get_functions(item)
        assert (len(temp) == 3)
        for func in list(temp.values()):
            assert callable(func), 'The function is not callable'


def test_get_function_global(global_module_data):
    for item in global_module_data.objectives:
        print(item)
        temp = gof_python.get_functions(item)
        assert (len(temp) == 3)
        for func in list(temp.values()):
            assert callable(func), 'The function is not callable'
