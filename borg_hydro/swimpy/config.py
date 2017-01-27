#!/usr/bin/python
######################################################################

#       Filename: config.py

#       Author: Stefan Luedtke

######################################################################

import os
import json
import jsonschema
import pkg_resources

######################################################################


# --------------------------
class swim_setup():
    '''
    A class that holds all the general configs given by the json file.
    '''
    # --------------------------
    
    @staticmethod
    def validate_config(self):
        '''
        Function to validate the user model configuration with the required
        jsonschema that is defined with the module.
        '''
        # Read the schema that is stored in this directory. This will be used
        # to validate the user given configuration.
        schema_file = pkg_resources.resource_filename(__name__,
                                                    'config_schema.json')
        with open(schema_file) as json_file:
            config_schema = json.load(json_file)
        # Validate the json schema. NOTE: the function only raises an error if 
        # the validation fails.
        try:
            jsonschema.validate(self.config_data, config_schema)
        except jsonschema.ValidationError:
            print("The configuratioin is not valid")

    def __init__(self, config_file):
        ''' Initialization of the model components.'''
        # Read json file
        with open(config_file) as json_file:
            self.config_data = json.load(json_file)
        # Validate the configuration
        self.validate_config(self)
        # get the first slot that hold general setup data
        general = self.config_data['general']
        # address project name
        self.pn = self.config_data['general']['project_name']
        # address project path
        self.pp = self.config_data['general']['project_path']
        # the string that specifies the model - most likely a python function
        self.model = self.config_data['general']['model']
        # get the path of the current working directory
        self.cwd = os.getcwd() + '/'

        # --------------------------
        parameter = self.config_data['parameters']
        # --------------------------
        # get the parameter list and format it for borg
        self.para_names = [para['name'] for para in parameter['list']]

        # get parameter regions (subcatchments in SWIM language), if that is
        # not provided, we set it to 1
        try:
            npreg = parameter['number_parameter_region']
        except KeyError:
            npreg = 1
        self.para_npreg = npreg

        # get parameter min and max
        parameter_min = [para['min'] for para in parameter['list']]
        parameter_max = [para['max'] for para in parameter['list']]
        # combine to list of min max values and repeat with the number of
        # parameter regions
        self.para_limits = list(map(list, zip(parameter_min, parameter_max))) *\
            self.para_npreg
        # parameter filename
        self.parameter_file = parameter['parameter_file']
        # --------------------------
        # get the objectives as a list of dicts
        self.objectives = list(objs for objs in
                               self.config_data['objectives']['list'])
        # --------------------------
        # get the evaluation period if provided
        try:
            temp = self.config_data['objectives']['evaluation_period']
            self.start = temp['start_date']
            self.end = temp['end_date']
            self.format = temp['format']
        except KeyError:
            print("\n----------------------------------------------\n")
            print("No start and end date are given, the entire simulation\
                    period will be evaluated")
            print("\n----------------------------------------------\n")
