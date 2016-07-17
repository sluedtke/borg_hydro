#!/usr/bin/python
# show commands being executed, per debug
#
######################################################################

#       Filename: test.py

#       Author: Stefan Luedtke

######################################################################

from python_libs.libsswim import gof_python

obs = r'./runoff_gof.dat'
sim = r'./mc_results/stat_dis_out_0001.csv'

test_obs =  gof_python.read_observed(obs)
t_sim = gof_python.read_simulated(sim)
