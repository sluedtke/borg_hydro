#!/usr/bin/python
# show commands being executed, per debug
#
######################################################################

#       Filename: test_gof.py

#       Author: Stefan Luedtke

######################################################################

from python_libs.libsswim import gof_python

######################################################################


# Testing the path for the observed file
def test_obs():
    obs = r'./runoff_gof.dat'
    test_obs = gof_python.read_observed(obs)


# Testing the path for the simulated file
def test_sim():
    sim = r'./mc_results/stat_dis_out_0001.csv'
    test_sim = gof_python.read_simulated(sim)
