#!/usr/bin/python
# show commands being executed, per debug
#
######################################################################

#       Filename: conftest.py

#       Author: Stefan Luedtke

######################################################################

import pytest
from swimpy import config

######################################################################


@pytest.fixture(scope="session")
def config_setup():
    '''test '''
    config_file = './tests/test_data_config/config.json'
    temp = config.swim_setup(config_file)
    return(temp)


@pytest.fixture(scope="session")
def config_para():
    '''test '''
    config_file = './tests/test_data_config/config.json'
    temp = config.swim_parameter(config_file)
    return(temp)


@pytest.fixture(scope="session")
def config_obj():
    '''test '''
    config_file = './tests/test_data_config/config.json'
    temp = config.swim_objectives(config_file)
    return(temp)


@pytest.fixture(scope="session")
def config_mo_setup():
    '''test '''
    config_file = './tests/test_data_config/config_mo.json'
    temp = config.swim_setup(config_file)
    return(temp)


@pytest.fixture(scope="session")
def config_mo_para():
    '''test '''
    config_file = './tests/test_data_config/config_mo.json'
    temp = config.swim_parameter(config_file)
    return(temp)


@pytest.fixture(scope="session")
def config_mo_obj():
    '''test '''
    config_file = './tests/test_data_config/config_mo.json'
    temp = config.swim_objectives(config_file)
    return(temp)


@pytest.fixture(scope="session")
def global_module_para():
    '''test '''
    config_file = './tests/test_data_config/global_module.json'
    temp = config.swim_parameter(config_file)
    return(temp)


@pytest.fixture(scope="session")
def global_module_obj():
    '''test '''
    config_file = './tests/test_data_config/global_module.json'
    temp = config.swim_objectives(config_file)
    return(temp)


@pytest.fixture(scope="session")
def global_module_setup():
    '''test '''
    config_file = './tests/test_data_config/global_module.json'
    temp = config.swim_setup(config_file)
    return(temp)


@pytest.fixture(scope="session")
def multi_station_para():
    '''test '''
    config_file = './tests/test_data_config/multi_station.json'
    temp = config.swim_parameter(config_file)
    return(temp)


@pytest.fixture(scope="session")
def multi_station_obj():
    '''test '''
    config_file = './tests/test_data_config/multi_station.json'
    temp = config.swim_objectives(config_file)
    return(temp)


@pytest.fixture(scope="session")
def multi_station_setup():
    '''test '''
    config_file = './tests/test_data_config/multi_station.json'
    temp = config.swim_setup(config_file)
    return(temp)
