#!/usr/bin/python
# #####################################################################

#       Filename: start_borg.py

#       Author: Stefan Luedtke

# #####################################################################

# =====================================================================
# == Import global modules
# =====================================================================

from borg_hydro.swimpy import gof_python, config, utils
import glob
import pandas as pd
import numpy as np

# =====================================================================
# Defining some general points  (dirs .. )
# =====================================================================
if __name__ == "__main__":
    base_dir = os.path.realpath(__file__)
# =====================================================================

config_file = "./borg_hydro/swimpy/tests/test_data_config/multi_station.json"
a = config.swim_setup(config_file)
b = config.swim_objectives(config_file)
c = config.swim_parameter(config_file)

item = b.objectives[0]
# call the function that makes concatenates the module and functions to
# something that can be applied
functions = utils.get_functions(item)
# call the USER function to read the observations
obs_file = glob.glob(str(a.pp) + '/' + item['obs_fp'])[0]
test_obs = functions['read_obs']['exe'](obs_file)
# call the USER function to read the simulations
sim_file = glob.glob(str(a.pp) + '/' + item['sim_fp'])[0]
test_sim = functions['read_sim']['exe'](sim_file)


temp = gof_python.obs_sim_merge(test_obs, test_sim)
result = functions['gof_func']['exe'](test_obs, test_sim)

config_file = "./borg_hydro/swimpy/tests/test_data_config/config_mo.json"
a = config.swim_setup(config_file)


config_file = "./borg_hydro/swimpy/tests/test_data_config/config.json"
a = config.swim_setup(config_file)
b = config.swim_objectives(config_file)
utils.compute_gof(a, b)

