#!/usr/bin/python
######################################################################

#       Filename: config.py

#       Author: Stefan Luedtke

######################################################################

import os
import json
import jsonschema
import pandas as pd
import pkg_resources

######################################################################


# --------------------------
class swim_setup(object):
    '''
    A class that holds all the general configs given by the json file.
    '''

    def check_para_names(self):
        '''
        Function that  checkes whether the supplied paramter names from the
        config exist in the template.
        '''
        unique_names = set(self.para_names)
        # intersection
        temp = set(self.para_names).intersection(self._para_names)
        if len(temp) != len(unique_names):
            raise KeyError("Configuration parameters not found.")
        else:
            pass

    # --------------------------
    def read_para_file(self):
        '''
        That function reads the parameter file from project.
        '''
        para_template = pd.read_csv(self.parameter_file, sep='\t', index_col=0)
        return(para_template)

    # --------------------------
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
            raise
    
    # --------------------------
    def __init__(self, config_file):
        ''' Initialization of the model components.'''
        # Read json file
        with open(config_file) as json_file:
            self.config_data = json.load(json_file)
        # Validate the configuration
        self.validate_config()
        # address project name
        self.pn = self.config_data['general']['project_name']
        # address project path
        self.pp = os.getcwd() + '/' +\
            self.config_data['general']['project_path']

        # --------------------------
        parameter = self.config_data['parameters']
        # --------------------------
        # set the paramater file path to self
        self.parameter_file = self.pp + '/' + parameter['parameter_file']
        # create the parameter template from the project parameter file
        self.para_template = self.read_para_file()
        # get parameter regions (subcatchments in SWIM language), if that is
        # not provided, we set it to 1
        self.para_npreg = len(parameter['parameter_region_ids'])
        self.para_preg_ids = parameter['parameter_region_ids']
        # get the parameter list and format it for borg
        self.para_names = [para['name'] for para in parameter['list']] *\
            self.para_npreg
        # create a list of variable names that is used only internaly
        self._para_names = ['ecal', 'thc', 'roc2', 'roc4', 'cncor',
                            'sccor', 'tsnfall', 'tmelt', 'smrate',
                            'gmrate', 'bff', 'abf', 'delay', 'revapc',
                            'rchrgc', 'revapmn']
        self.check_para_names()
        # get parameter min and max
        parameter_min = [para['min'] for para in parameter['list']]
        parameter_max = [para['max'] for para in parameter['list']]
        # combine to list of min max values and repeat with the number of
        # parameter regions
        self.para_limits = list(map(list, zip(parameter_min, parameter_max)))\
            * self.para_npreg
        # --------------------------
        # get the objectives as a list of dicts
        self.objectives = list(objs for objs in
                               self.config_data['objectives']['list'])
        # --------------------------
        # get the evaluation period if provided
        # that are the keys we want to have from the slot evaluation_period
        key_list = ["start_date", "end_date", "format"]
        try:
            temp = self.config_data['objectives']['evaluation_period']
        except KeyError:
            # if evaluation_period is not present at all, set all values for 
            # that slot to None
            temp = dict(zip(key_list,  [None, None, None]))
        ev = []
        # Check whether the single elements are set or not 
        for k in key_list:
            if k in temp:
                ev.append(temp[k])
            else:
                ev.append(None)
        # create a dict with the keys defined above
        ev = dict(zip(key_list, ev))
        # assign them to our configuration object
        self.start = ev['start_date']
        self.end = ev['end_date']
        self.format = ev['format']
