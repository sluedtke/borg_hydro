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
    obs_file = r'./borg_hydro/swimpy/tests/test_data_gof/runoff_gof.dat'
    obs = utils.read_observed(obs_file)
    return(obs)


@pytest.fixture(scope="session")
def read_sim():
    ''' Just a fixture to read the files for further testing'''
    sim_file = r'./borg_hydro/swimpy/tests/test_data_gof/mc_results/stat_dis_out_0001.csv'
    sim = utils.read_simulated(sim_file)
    return(sim)


@pytest.fixture(scope="session")
def config_setup():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_data_config/config.json'
    temp = config.swim_setup(config_file)
    return(temp)


@pytest.fixture(scope="session")
def config_para():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_data_config/config.json'
    temp = config.swim_parameter(config_file)
    return(temp)


@pytest.fixture(scope="session")
def config_obj():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_data_config/config.json'
    temp = config.swim_objectives(config_file)
    return(temp)


@pytest.fixture(scope="session")
def config_mo_setup():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_data_config/config_mo.json'
    temp = config.swim_setup(config_file)
    return(temp)


@pytest.fixture(scope="session")
def config_mo_para():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_data_config/config_mo.json'
    temp = config.swim_parameter(config_file)
    return(temp)


@pytest.fixture(scope="session")
def config_mo_obj():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_data_config/config_mo.json'
    temp = config.swim_objectives(config_file)
    return(temp)


@pytest.fixture(scope="session")
def global_module_para():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_data_config/global_module.json'
    temp = config.swim_parameter(config_file)
    return(temp)


@pytest.fixture(scope="session")
def global_module_obj():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_data_config/global_module.json'
    temp = config.swim_objectives(config_file)
    return(temp)


@pytest.fixture(scope="session")
def global_module_setup():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_data_config/global_module.json'
    temp = config.swim_setup(config_file)
    return(temp)


@pytest.fixture(scope="session")
def multi_station_para():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_data_config/multi_station.json'
    temp = config.swim_parameter(config_file)
    return(temp)


@pytest.fixture(scope="session")
def multi_station_obj():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_data_config/multi_station.json'
    temp = config.swim_objectives(config_file)
    return(temp)


@pytest.fixture(scope="session")
def multi_station_setup():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_data_config/multi_station.json'
    temp = config.swim_setup(config_file)
    return(temp)

# config that has date with no errors
@pytest.fixture(scope="session")
def no_error_para():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_data_config/config_no_error.json'
    temp = config.swim_parameter(config_file)
    return(temp)


@pytest.fixture(scope="session")
def no_error_obj():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_data_config/config_no_error.json'
    temp = config.swim_objectives(config_file)
    return(temp)


@pytest.fixture(scope="session")
def no_error_setup():
    '''test '''
    config_file = './borg_hydro/swimpy/tests/test_data_config/config_no_error.json'
    temp = config.swim_setup(config_file)
    return(temp)


@pytest.fixture(scope="session")
def obs_simple():
    ''' Creating 2 DataFrame with with the same entry at every timestep'''
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
    ''' Creating 2 DataFrame with with the same entry at every timestep'''
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
def read_para_example():
    ''' Just a fixture to read the files for further testing'''
    temp = r'./borg_hydro/swimpy/tests/test_data_gof/regpar0001.dat'
    para = pd.read_csv(temp, sep=" ")
    para_list = list(map(float, list(para)))
    return(para_list)
