#!/usr/bin/python
######################################################################

#       Filename: utils.py

#       Author: Stefan Luedtke

######################################################################

import pandas as pd
import numpy as np
import glob
from . import gof_python

######################################################################


# --------------------------
def read_observed(obs_file):
    '''
    That function takes a single file name from the observed data and reads
    this as pandas data frame. Currently, only a single columns holds the data
    (the second one) and the first one is the date and index column.

    Return value is a pandas dataframe
    '''

    temp = pd.read_csv(obs_file, sep='\t', index_col='date',
                       parse_dates=['date'],
                       na_values=[-9999, -999, -99])
    return(temp)


# ----------------------------
def read_simulated(simu_file):
    '''
    That function takes a single file name from the simulated data and reads
    this as pandas data frame. Currently, only a single columns holds the data
    (the third one) and the first two the date and thus the index column.

    Return value is a pandas dataframe
    '''

    dateparse = lambda y, d: pd.datetime.strptime(''.join([y, d]), '%Y%j')

    temp = pd.read_csv(simu_file, index_col='date',
                       delim_whitespace=True,
                       parse_dates={'date': ['YEAR', 'DAY']},
                       date_parser=dateparse,
                       na_values=[-9999, -999, -99])
    return(temp)


# ---------------------------------------------
def window_ts(pandas_df, start_date, end_date):
    '''
    This function takes a pandas dataframe, a start and an end date and
    returns the df starting with start_date and ending with end_date.

    Return value is a pandas dataframe
    '''
    # Create an index with the new date range
    temp_index = pd.date_range(start=start_date, end=end_date)
    # Use that index to clip the input data frame
    pandas_df = pandas_df.loc[temp_index]
    return(pandas_df)


# -----------------------------------
def search_function(func, mod):
    '''
    I do not like this one :-(. It takes the given module and the function
    string and build and callable object. If the module is given in several
    parts, e.g. "part1.part2", we need to call *getattr* several times and
    using the output from the previous evaluation. I am missing the correct
    word right now. 

    >>> a = search_function(func='equals', mod='pd.DataFrame')
    >>> a.__module__ + '.' + a.__name__
    'pandas.core.generic.equals'
    '''

    temp = mod.split('.')
    temp.append(func)
    mod = temp[0]
    exe = globals()[mod]
    for i in range(1, len(temp)):
        exe = getattr(exe, temp[i])
    try:
        callable(exe)
    except NameError:
        print('The given module and function can not be found. Make sure the\
               base module is imorted')
    return(exe)


# -----------------------------------
def get_functions(item):
    '''
    A function that get the function and module names from the config and puts
    them into a list of callable objects. We have to test at which scope each
    variable is available. Not very nice style, but it works for now.

    Return value is a list of three functions.
    '''
    # Create a dictionary that is later extended by the callable ojbect
    input_dict = {'read_obs':
                      {'mod': item['read_module'],
                      'func': item['read_obs_function']}, 
                  'read_sim':
                      {'mod': item['read_module'],
                      'func': item['read_sim_function']},
                  'gof_func':
                      {'mod': item['gof_module'],
                      'func': item['gof_function']}}

    for i in input_dict.keys():
        func = input_dict[i]['func']
        mod = input_dict[i]['mod']
        # check whether the function is already accessible in the current
        # namespace
        try:
            exe = globals()[func]
        # if not, call the function that splits the module and iterates of each
        # component until it reaches the function *func*
        except KeyError:
            exe = search_function(func, mod)
        # put the result to the current dict entry with the key 'exe'.
        input_dict[i]['exe'] = exe
    # return the whole dictionary
    # TODO: we should call that during the initialization when we create the
    # 'swim_objectives' object
    return(input_dict)


# -----------------------------------
def compute_gof(swim_setup, swim_objectives):
    '''
    For each objectives in the config the functions computes the performance as
    specified in the config.

    Returns a list with one value for each objective.
    '''
    result_list = []
    for item in swim_objectives.objectives:
        # call the function that makes concatenates the module and functions to
        # something that can be applied
        functions = get_functions(item)
        # call the USER function to read the observations
        obs_file = glob.glob(str(swim_setup.pp) + '/' + item['obs_fp'])[0]
        temp_obs = functions['read_obs']['exe'](obs_file)
        # call the USER function to read the simulations
        sim_file = glob.glob(str(swim_setup.pp) + '/' + item['sim_fp'])[0]
        temp_sim = functions['read_sim']['exe'](sim_file)
        # call the USER function to compute the performance
        result = functions['gof_func']['exe'](temp_obs, temp_sim)
        # In case we have multiple  station, apply a function to aggregate them
        # And append to the list that is returned
        result_list.append(result)
    return(result_list)


def write_parameter_file(para_list, swim_config, swim_para):
    '''
    This function takes a list of parameters and writes them to a file given
    via the swim_parameter class.
    '''
    # Convert to numpy array
    regpar = np.asarray(para_list)
    # reshape
    regpar = np.ndarray.reshape(regpar, (-1, swim_para.npreg)).T
    # write fixed format style
    para_file = swim_config.pp + '/' + swim_para.parameter_file
    np.savetxt(para_file, regpar, fmt='%.4f')
