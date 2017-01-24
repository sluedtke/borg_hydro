#!/usr/bin/python
######################################################################

#       Filename: gof_python.py

#       Author: Stefan Luedtke

######################################################################

import pandas as pd
import numpy as np


######################################################################
def nse(temp_obs, temp_sim):
    '''
    This function computes the  Nash-Sutcliffe-Efficiency between the observed
    and simulated discharge.
    nse = 1 - ( ( sum ( obs(t) - sim(t))^2) / ( sum ( obs(t) - mean(obs)) ^2)
                        -------- A --------                   ---- C ---
                 ----- B ------------------  -- E -- --------- D -----------
        ------------------------------ F ------------------------------------
    Return value is a float.

    '''
    # Join the dataframes to get rid of NA values
    mp = obs_sim_merge(temp_obs, temp_sim)
    mp = mp.set_index(['date'])
    # ----------------------
    # Numerator
    # Squared difference
    # - A
    mp['numerator'] = np.square(mp['sim'] - mp['obs'])
    # Sum of squared differences
    # - B
    numerator = mp.groupby(['station']).aggregate({'numerator': np.sum}).copy()
    # ----------------------
    # Denominator
    # - C
    obs_mean = mp.groupby(['station']).aggregate({'obs':
                                                  np.mean}).reset_index()
    obs_mean.columns = ['station', 'obs_mean']
    temp_denom = pd.merge(mp.reset_index()[['station', 'obs']],
                          obs_mean)
    # - D
    temp_denom['denominator'] = np.square(temp_denom['obs']-temp_denom['obs_mean'])
    denominator = temp_denom.groupby(['station']).aggregate({'denominator':
                                                             np.sum}).copy()
    # - E
    temp = pd.merge(numerator.reset_index(), denominator.reset_index())
    # - F
    temp['obj'] = 1 - temp['numerator']/temp['denominator']
    # ----------------------
    result = np.mean(temp['obj'].dropna())
    return(result)


# -----------------------------------
def log_rmse(temp_obs, temp_sim):
    '''
    This function computes the log-Root-Means-Square-Error (rmse) between the
    log of the simulated and  the log of the observed time series. That is
    defined as:

    rmse = sqrt( mean( (sim - obs)^2)

    Return value is a float.
    '''
    # Join the dataframes to get rid of NA values
    mp = obs_sim_merge(temp_obs, temp_sim)
    mp = mp.set_index(['date'])

    # replace all zeros with NaN
    mp['sim'] = mp['sim'].replace(0, np.nan)
    mp['obs'] = mp['obs'].replace(0, np.nan)

    # Apply the log (ln) transform to both columns
    mp['sim'] = np.log(mp['sim'])
    mp['obs'] = np.log(mp['obs'])
    # Squared difference
    mp['obj'] = np.square(mp['sim'] - mp['obs'])
    # mean
    temp = mp.groupby(['station']).aggregate({'obj': np.mean})
    # Square root of the mean of differences
    temp = pd.DataFrame(np.sqrt(temp['obj']))
    result = np.mean(temp['obj'])
    return(result)


# ----------------------------------------
def obs_sim_merge(pandas_obs, pandas_sim):
    '''
    This function takes tow pandas dataframes and merges them into a single
    one. The new column names are "obs" and "sim". The join or merge will be
    based on the timestamp of the observed data set only and NA values will be
    dropped.

    Return value is a pandas dataframe
    '''
    # Melt both data frames into a long format
    temp_obs = pandas_obs.reset_index()
    temp_obs = pd.melt(temp_obs, id_vars=['date'], var_name='station',
                       value_name='obs')
    temp_sim = pandas_sim.reset_index()
    temp_sim = pd.melt(temp_sim, id_vars=['date'], var_name='station',
                       value_name='sim')
    # Merge them based on the index
    temp = pd.merge(left=temp_obs, right=temp_sim).dropna()
    return(temp)
