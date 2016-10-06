#!/usr/bin/python
# show commands being executed, per debug
#
######################################################################

#       Filename: test_config.py

#       Author: Stefan Luedtke

######################################################################

import pytest
from swimpy import config

######################################################################


def test_read_config():
    '''test '''
    config_file = './tests/test_data_config/config.json'
    temp = config.user_borg_model(config_file)
    assert isinstance(temp, config.user_borg_model), 'Wrong data type'


@pytest.fixture()
def read_config():
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
def read_config_mo():
    '''test '''
    config_file = './tests/test_data_config/config_mo.json'
    temp = config.user_borg_model(config_file)
    return(temp)


def test_parse_objectives(read_config_mo, read_config):
    '''test '''
    assert (len(read_config_mo.objectives) == 4), 'Wrong number of objectives'
    assert (len(read_config.objectives) == 2), 'Wrong number of objectives'
