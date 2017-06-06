#!/usr/bin/python
######################################################################

#       Filename: utils.py

#       Author: Stefan Luedtke

######################################################################

import sys
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
                       na_values=[-9999, -999, -99, 'NaN', -999.000])
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
                       na_values=[-9999, -999, -99, 'NaN', -999.000])
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


def check_overlap(pandas_obs, pandas_sim):
    '''
    A function that checkt whether the simulation and observation  share common
    ground in terms of time.
    This function exits if it does not find any overlap.
    '''
    # find maximum date from the observation
    obs_end = pandas_obs.index.max().date()
    obs_start = pandas_obs.index.min().date()
    # find minimum date from the simulation
    sim_start = pandas_sim.index.min().date()
    sim_end = pandas_sim.index.max().date()
    if ((obs_end <= sim_start) | (sim_end <= obs_start)):
        sys.exit("The time series do not overlap, exiting")
    else:
        return('overlap found')


# -----------------------------------
def only_numbers(python_list):
    '''
    A function that takes a python list and returns a list that contains only numbers. 
    All strings are silently dropped.
    Examples:
    >>> # numbers and string
    >>> only_numbers([1, 2, 'kfdsajk'])
    [1.0, 2.0]
    >>> # numbers (as strings)  and string
    >>> only_numbers(['1', '2', 'kfdsajk'])
    [1.0, 2.0]
    >>> # numbers (as strings)
    >>> only_numbers(['1', '2', '3'])
    [1, 2, 3]
    >>> # only numbers
    >>> only_numbers([1, 2, 3])
    [1, 2, 3]
    >>> # numbers and NaN
    >>> only_numbers(['1', '2', np.nan])
    [1.0, 2.0]
    '''
    temp = np.array(python_list)
    temp = pd.to_numeric(temp, errors='coerce')
    temp = temp[~np.isnan(temp)].tolist()
    return(temp)


# -----------------------------------
def aggregator_function(numeric_list):
    '''
    A function that computes the median of a list of numeric value.
    >>> aggregator_function([2, 3])
    2.5
    >>> aggregator_function([3, 3])
    3.0
    >>> aggregator_function([3, 3, 3])
    3.0
    >>> aggregator_function([1, 2, 3])
    2.0
    '''
    temp = np.array(numeric_list)
    temp = np.median(temp)
    return(temp)


# -----------------------------------
def compute_gof(swim_config):
    '''
    For each objectives in the config the functions computes the performance as
    specified in the config.

    Returns a list with one value for each objective.
    NOTE: If a single objective has multiple stations, a performance measure
    for each station is returned.
    Examples with dummy values:
    1) one objective with a single station:
    [[gof_value_1]]

    2) one objective with a three station:
    [[gof_value_1, gof_value_2, gof_value_3]]

    3) two objectives with a one station:
    [[gof_value_1], [gof_value_2]]

    4) two objectives with a two and three stations respectively 
    [[gof_value_1, gof_value_2], [gof_value_3, gof_value_4, gof_value_5]]

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
        # check whether there is ov     import pdb; pdb.set_trace()erlap between both time series at all
        test  = check_overlap(temp_obs, temp_sim)
        # call the USER function to compute the performance
        result = functions['gof_func']['exe'](temp_obs, temp_sim)
        # append to the list that is returned
        result_list.append(result)
    return(result_list)


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
def create_para_borg(swim_config, parameter_list):
    '''
    That function will create a pandas data frame based on the parameter list.
    It will use the class attribute 'para_names' as names and the attribute
    'para_npreg' to create the data frame with the shape len(para_names) by
    para_npreg (columns x rows).
    A pandas data frame is parsed and used to update the parameter template of
    the class.
    '''
    # split the list into equally sized chunks
    temp_list = np.array_split(parameter_list, swim_config.para_npreg)
    temp_list = [temp_list[i].tolist() for i in range(len(temp_list))]

    # create the dataframe
    columns = sorted(set(swim_config.para_names), key=swim_config.para_names.index)
    para_pd = pd.DataFrame(temp_list, columns=columns)
    # create column for the catchment id
    para_pd['catchmentID'] = para_pd.index
    para_pd.catchmentID = para_pd.catchmentID + 1
    para_pd = para_pd.set_index('catchmentID')
    para = swim_config.para_template
    para.update(para_pd, join='left')
    para_borg = para.reset_index(drop=False)
    return(para_borg)


# --------------------------
def write_parameter_file(swim_config, parameter_borg):
    '''
    This method just writes the newly created parameter set to file. This
    attribute is empty if not set before by parsing a list of parameters.
    '''
    para_file = swim_config.pp + '/' + swim_config.parameter_file
    parameter_borg.to_csv(para_file, sep='\t', encoding='utf-8',
                                 header=True, index=False)
