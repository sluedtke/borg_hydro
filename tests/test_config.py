#!/usr/bin/python
# show commands being executed, per debug
#
######################################################################

#       Filename: test_config.py

#       Author: Stefan Luedtke

######################################################################

import pytest
from python_libs.libsswim import config

######################################################################


def test_read_config():
    '''test '''
    config_file = './tests/test_data/config.json'
    temp = config.user_borg_model(config_file)
    assert isinstance(temp, config.user_borg_model), 'Wrong data type'


@pytest.fixture()
def read_config():
    '''test '''
    config_file = './tests/test_data/config.json'
    temp = config.user_borg_model(config_file)
    assert isinstance(temp, config.user_borg_model), 'Wrong data type'