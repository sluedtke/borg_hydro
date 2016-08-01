#!/usr/bin/python
######################################################################

#       Filename: config.py

#       Author: Stefan Luedtke

######################################################################

import json

######################################################################


# --------------------------
class user_borg_model():
    '''
    A class that holds all the configs given by the json file. Not sure whether
    that is all a bit overkill, lets see
    '''
    def __init__(self, config_file):
        # ''' Initialization of the model components '''
        # read the json file with the config
        with open(config_file) as json_file:
            config_data = json.load(json_file)
        # address project name
        self.pn = config_data['project_name']
        # address project path
        self.pp = config_data['project_path']
        # address result path
        self.rp = config_data['result_path']
        #
        # get the parameter list and format it for borg
        self.para_names = [para['name'] for para in config_data['parameters']]
        # get parameter min and max
        parameter_min = [para['min'] for para in config_data['parameters']]
        parameter_max = [para['max'] for para in config_data['parameters']]
        self.parameter_list = list(map(list, zip(parameter_min, parameter_max)))
