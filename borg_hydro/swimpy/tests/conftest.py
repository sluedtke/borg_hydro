#!/usr/bin/python
# show commands being executed, per debug
#
######################################################################

#       Filename: conftest.py

#       Author: Stefan Luedtke

######################################################################

import pytest
import datetime
import pandas as pd
from borg_hydro.swimpy import config, utils

######################################################################


@pytest.fixture(scope="session")
def read_obs():
    ''' Just a fixture to read the files for further testing'''
    obs_file = r'./borg_hydro/swimpy/tests/test_input/runoff_gof.dat'
    obs = utils.read_observed(obs_file)
    return(obs)


@pytest.fixture(scope="session")
def read_sim():
    ''' Just a fixture to read the files for further testing'''
    sim_file = r'./borg_hydro/swimpy/tests/test_output/Res/stat_dis_out_0001.csv'
    sim = utils.read_simulated(sim_file)
    return(sim)


# That one is modified during a test, to get the original one for all the 
# others, we use function scope
@pytest.fixture(scope="function")
def config_setup():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/config.json'
    temp = config.swim_setup(config_file)
    return(temp)


@pytest.fixture(scope="function")
def config_mo_setup():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/config_mo.json'
    temp = config.swim_setup(config_file)
    return(temp)


@pytest.fixture(scope="session")
def global_module_setup():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/global_module.json'
    temp = config.swim_setup(config_file)
    return(temp)


@pytest.fixture(scope="session")
def multi_station_setup():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/multi_station.json'
    temp = config.swim_setup(config_file)
    return(temp)


@pytest.fixture(scope="session")
def no_error_setup():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/config_no_error.json'
    temp = config.swim_setup(config_file)
    return(temp)


@pytest.fixture(scope="function")
def para_region_setup():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/para_region.json'
    temp = config.swim_setup(config_file)
    return(temp)


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
    return(obs_simple)


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
    return(sim_simple)


@pytest.fixture(scope="session")
def obs_some_zeros(obs_simple):
    '''
    Create a dataframe that has some zeros for testing log rmse.
    '''
    obs_temp = obs_simple.copy(deep=True)
    obs_temp.iloc[3:4, obs_temp.columns.get_loc('X10')] = 0
    return(obs_temp)


@pytest.fixture(scope="session")
def sim_some_zeros(sim_simple):
    '''
    Create a dataframe that has some zeros for testing log rmse.
    '''
    sim_temp = sim_simple.copy(deep=True)
    sim_temp.iloc[0:3, sim_temp.columns.get_loc('X10')] = 0
    return(sim_temp)


@pytest.fixture(scope="session")
def obs_sim_merge(obs_simple, sim_simple):
    temp = utils.obs_sim_merge(obs_simple, sim_simple)
    return(temp)


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
    return(obs_simple)


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
    return(sim_simple)


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
    return(obs_simple)


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
    return(sim_simple)
