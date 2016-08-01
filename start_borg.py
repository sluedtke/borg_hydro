#!/usr/bin/python
# #####################################################################

#       Filename: config.py

#       Author: Stefan Luedtke

# ############################   	PURPOSE		######################
# Set all the parts that we do have to change between the different model
# version we have to run. The aim is, to have one config file that defines the
# paths, ... so that all the other python files do not have to be changed as
# long as the model stays the same.
# #####################################################################

# =====================================================================
# == Import global modules
# =====================================================================

from python_libs.libsswim import gof_python, config


config_file = './config.json'
a = config.user_borg_model(config_file)
a.parameter_list

# =====================================================================
# Defining some general points  (dirs .. )
# =====================================================================
if __name__ == "__main__":
    base_dir = os.path.realpath(__file__)
# =====================================================================

exe = base_dir + "start_bsub_swim"
comp_jobs = help_dir + "compare_jobs.R"
clean = "rm ./log/* *gof.out"

