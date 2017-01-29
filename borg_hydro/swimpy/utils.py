#!/usr/bin/python
######################################################################

#       Filename: utils.py

#       Author: Stefan Luedtke

######################################################################

import pandas as pd
import numpy as np
import glob
import datetime
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
def convert_dates(date_var):
    # Break if start and end date are the same (or if nothing is given)
    date_var = str(date_var)
    try:
        date_var = datetime.datetime.strptime(date_var, "%Y-%m-%d").date()
    except ValueError:
        "The provided date string is not given in a standard format"
        raise
    return(date_var)


# ---------------------------------------------
def set_truncation_dates(*args):
    source_start, source_end = args[0], args[1]
    start_date, end_date = args[2], args[3]
    # do nothing if both values are None
    if (start_date is None) & (end_date is None):
        temp_start = source_start
        temp_end = source_end
    # use max(start_date, source_start) if end date is None. We use max
    # because we want to be bigger than the start date of the series
    elif end_date is None:
        temp_start = max(source_start, convert_dates(start_date))
        temp_end = source_end
    # use min(end_date, source_end) if start date is None. We use min
    # because we want to be smaller than the end date of the series
    elif start_date is None:
        temp_start = source_start
        temp_end = min(source_end, convert_dates(end_date))
    # if both are given and start is smaller
    elif convert_dates(start_date) < convert_dates(end_date):
        temp_start = max(source_start, convert_dates(start_date))
        temp_end = min(source_end, convert_dates(end_date))
    elif convert_dates(start_date) >= convert_dates(end_date):
        raise SystemExit("Start date can not be bigger or equal to end date")
    return([temp_start, temp_end])


# ---------------------------------------------
def window_ts(pandas_df, start_date=None, end_date=None):
    '''
    This function takes a pandas dataframe, a start and an end date and
    returns the df starting with start_date and ending with end_date.

    Return value is a pandas dataframe
    '''
    # get start and end date from the time series at hand
    source_start = pandas_df.index.min().date()
    source_end = pandas_df.index.max().date()
    # create the args list that is parsed to the function call
    args = [source_start, source_end, start_date, end_date]
    temp_start, temp_end = set_truncation_dates(*args)
    # NOTE: the word truncate does not mean include
    pandas_df = pandas_df.truncate(before=temp_start, after=temp_end)
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
def compute_gof(swim_config):
    '''
    For each objectives in the config the functions computes the performance as
    specified in the config.

    Returns a list with one value for each objective.
    '''
    result_list = []
    for item in swim_config.objectives:
        # call the function that makes concatenates the module and functions to
        # something that can be applied
        functions = get_functions(item)
        # call the USER function to read the observations
        obs_file = glob.glob(str(swim_config.pp) + '/' + item['obs_fp'])[0]
        temp_obs = functions['read_obs']['exe'](obs_file)
        # call the USER function to read the simulations
        sim_file = glob.glob(str(swim_config.pp) + '/' + item['sim_fp'])[0]
        temp_sim = functions['read_sim']['exe'](sim_file)
        # Try to apply the window function to the simulated time series
        try:
            temp_sim = window_ts(temp_sim, start_date=swim_config.start,
                                 end_date=swim_config.end)
        except AttributeError:
            temp_sim = temp_sim
        # call the USER function to compute the performance
        result = functions['gof_func']['exe'](temp_obs, temp_sim)
        # append to the list that is returned
        result_list.append(result)
    return(result_list)


# -----------------------------------
def write_parameter_file(para_list, swim_config):
    '''
    This function takes a list of parameters and writes them to a file given
    via the swim_parameter class.
    '''
    # Convert to numpy array
    regpar = np.asarray(para_list)
    # format the list with respect to the number of parameter regions
    regpar = np.tile(regpar, (swim_config.para_npreg, 1))
    regpar = pd.DataFrame(regpar)
    regpar.insert(0, 'a', 1)
    regpar.insert(regpar.shape[1], 'b', 1)
    regpar.columns = ['catchmentID'] + swim_config.para_names + ['stationID']
    para_file = swim_config.pp + '/'+ swim_config.parameter_file
    regpar.to_csv(para_file, sep='\t', encoding='utf-8', header=True,
                  index=False)
