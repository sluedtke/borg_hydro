#!/usr/bin/python
'''
Setting up fixtures that will be used for the unit tests.
'''

#
######################################################################

#       Filename: conftest.py

#       Author: Stefan Luedtke

######################################################################

import datetime
import pytest
import pandas as pd
from borg_hydro.swimpy import config, utils

######################################################################


# --------------------------------------------------------------------------
@pytest.fixture(scope="session")
def config_01():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_configs/01-config.json'
    temp = config.swim_setup(config_file)
    return temp


@pytest.fixture(scope="session")
def config_02():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_configs/02-config.json'
    temp = config.swim_setup(config_file)
    return temp


@pytest.fixture(scope="session")
def config_03():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_configs/03-config.json'
    temp = config.swim_setup(config_file)
    return temp


@pytest.fixture(scope="session")
def config_04():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_configs/04-config.json'
    temp = config.swim_setup(config_file)
    return temp


@pytest.fixture(scope="session")
def config_06():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_configs/06-config.json'
    temp = config.swim_setup(config_file)
    return temp


@pytest.fixture(scope="session")
def config_07():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_configs/07-config.json'
    temp = config.swim_setup(config_file)
    return temp


@pytest.fixture(scope="session")
def config_08():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_configs/08-config.json'
    temp = config.swim_setup(config_file)
    return temp


@pytest.fixture(scope="session")
def config_09():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_configs/09-config.json'
    temp = config.swim_setup(config_file)
    return temp


@pytest.fixture(scope="session")
def config_10():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_configs/10-config.json'
    temp = config.swim_setup(config_file)
    return temp


# collect all of them into a dict .. I hope thats easier to use later on
@pytest.fixture(scope="session")
def config_dict(config_01, config_02, config_03, config_04, config_06,
                config_07, config_08, config_09, config_10):
    '''test '''
    temp = dict()
    temp["config_01"] = config_01
    temp["config_02"] = config_02
    temp["config_03"] = config_03
    temp["config_04"] = config_04
    temp["config_06"] = config_06
    temp["config_07"] = config_07
    temp["config_08"] = config_08
    temp["config_09"] = config_09
    temp["config_10"] = config_10
    return temp


# --------------------------------------------------------------------------
@pytest.fixture(scope="session")
def read_obs():
    ''' Just a fixture to read the files for further testing'''
    obs_file = r'./borg_hydro/swimpy/tests/test_input/runoff_gof.dat'
    obs = utils.read_observed(obs_file)
    return obs


@pytest.fixture(scope="session")
def read_sim():
    ''' Just a fixture to read the files for further testing'''
    sim_file = r'./borg_hydro/swimpy/tests/test_output/Res/stat_dis_out_0001.csv'
    sim = utils.read_simulated(sim_file)
    return sim


@pytest.fixture(scope="session")
def obs_simple():
    ''' Creating a DataFrame with with the same entry at every timestep'''
    todays_date = datetime.datetime.now().date()
    date = pd.date_range(todays_date-datetime.timedelta(10), periods=14,
                         freq='D')
    columns = ['X10']
    obs_simple = pd.DataFrame(columns=columns)
    obs_simple['date'] = date
    obs_simple = obs_simple.fillna(1)
    obs_simple = obs_simple.set_index(['date'])
    return obs_simple


@pytest.fixture(scope="session")
def sim_simple():
    ''' Creating a DataFrame with with the same entry at every timestep'''
    todays_date = datetime.datetime.now().date()
    date = pd.date_range(todays_date-datetime.timedelta(10), periods=14,
                         freq='D')
    columns = ['X10']
    sim_simple = pd.DataFrame(columns=columns)
    sim_simple['date'] = date
    sim_simple = sim_simple.fillna(1)
    sim_simple = sim_simple.set_index(['date'])
    return sim_simple


@pytest.fixture(scope="session")
def obs_some_zeros(obs_simple):
    '''
    Create a dataframe that has some zeros for testing log rmse.
    '''
    obs_temp = obs_simple.copy(deep=True)
    obs_temp.iloc[3:4, obs_temp.columns.get_loc('X10')] = 0
    return obs_temp


@pytest.fixture(scope="session")
def sim_some_zeros(sim_simple):
    '''
    Create a dataframe that has some zeros for testing log rmse.
    '''
    sim_temp = sim_simple.copy(deep=True)
    sim_temp.iloc[0:3, sim_temp.columns.get_loc('X10')] = 0
    return sim_temp


@pytest.fixture(scope="session")
def obs_sim_merge(obs_simple, sim_simple):
    temp = utils.obs_sim_merge(obs_simple, sim_simple)
    return temp


@pytest.fixture(scope="session")
def obs_simple_1():
    ''' Creating a DataFrame with with the same entry at every timestep'''
    todays_date = datetime.datetime.now().date()
    date = pd.date_range(todays_date-datetime.timedelta(10), periods=9,
                         freq='D')
    columns = ['X10']
    obs_simple = pd.DataFrame(columns=columns)
    obs_simple['date'] = date
    obs_simple['X10'] = range(1, 9 + 1, 1)
    obs_simple = obs_simple.set_index(['date'])
    return obs_simple


@pytest.fixture(scope="session")
def sim_simple_1():
    ''' Creating a DataFrame with with the same entry at every timestep'''
    todays_date = datetime.datetime.now().date()
    date = pd.date_range(todays_date-datetime.timedelta(10), periods=12,
                         freq='D')
    columns = ['X10']
    sim_simple = pd.DataFrame(columns=columns)
    sim_simple['date'] = date
    sim_simple = sim_simple.fillna(5)
    sim_simple = sim_simple.set_index(['date'])
    return sim_simple


@pytest.fixture(scope="session")
def obs_simple_2():
    ''' Creating a DataFrame with with the same entry at every timestep'''
    todays_date = datetime.datetime.now().date()
    date = pd.date_range(todays_date-datetime.timedelta(10), periods=9,
                         freq='D')
    columns = ['X10']
    obs_simple = pd.DataFrame(columns=columns)
    obs_simple['date'] = date
    obs_simple['X10'] = range(1, 9 + 1, 1)
    obs_simple = obs_simple.set_index(['date'])
    return obs_simple


@pytest.fixture(scope="session")
def sim_simple_2():
    ''' Creating a DataFrame with with the same entry at every timestep'''
    todays_date = datetime.datetime.now().date()
    date = pd.date_range(todays_date-datetime.timedelta(10), periods=9,
                         freq='D')
    columns = ['X10']
    sim_simple = pd.DataFrame(columns=columns)
    sim_simple['date'] = date
    sim_simple['X10'] = range(1, 9 + 1, 1)
    sim_simple['X10'] = sim_simple['X10'] * 2
    sim_simple = sim_simple.set_index(['date'])
    return sim_simple
