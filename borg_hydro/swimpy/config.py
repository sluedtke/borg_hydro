#!/usr/bin/python
######################################################################

#       Filename: config.py

#       Author: Stefan Luedtke

######################################################################

import os
import json
import jsonschema
import numpy as np
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
    def create_para_template(self):
        '''
        Function that creates a pandas dataframe that is used as a parameter
        template.
        '''
        para_values = [1.15, 1.0, 7.0, 7.0, 1, 2.500, 0.0, 0.0, 1.0, 1.0, 1.0,
                       0.04800, 200, 0.2000, 0.0500, 0.0]

        template = np.asarray(para_values)
        # format the list with respect to the number of parameter regions
        template = np.tile(template, (self.para_npreg, 1))
        template = pd.DataFrame(template)
        template.insert(0, 'a', [x+1 for x in range(self.para_npreg)])
        template.insert(template.shape[1], 'b', 'stationName')
        template.columns = ['catchmentID'] + self._para_names + ['stationID']
        para_template = template.set_index('catchmentID')
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
    @property
    def para_borg(self):
        return(self._para_borg)
        
    # --------------------------
    @para_borg.setter
    def para_borg(self, parameter_list):
        '''
        That function will create a pandas data frame based on the parameter list.
        It will use the class attribute 'para_names' as names and the attribute
        'para_npreg' to create the data frame with the shape len(para_names) by
        para_npreg (columns x rows).
        A pandas data frame is parsed and used to update the parameter template of
        the class.
        '''
        # create the dataframe
        para_pd = pd.DataFrame(parameter_list, columns=set(self.para_names))
        # create column for the catchment id
        para_pd['catchmentID'] = para_pd.index
        para_pd.catchmentID = para_pd.catchmentID + 1
        para_pd = para_pd.set_index('catchmentID')
        para = self.para_template
        para.update(para_pd, join='left')
        para = para.reset_index(drop=False)
        self._para_borg = para
        
    # --------------------------
    def write_parameter_file(self):
        '''
        This method just writes the newly created parameter set to file. This 
        attribute is empty if not set before by parsing a list of parameters.
        '''
        para_file = self.pp + '/' + self.parameter_file
        self.para_borg.to_csv(para_file, sep='\t', encoding='utf-8',
                                     header=True, index=False)

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
        # get parameter regions (subcatchments in SWIM language), if that is
        # not provided, we set it to 1
        try:
            npreg = parameter['number_parameter_region']
        except KeyError:
            npreg = 1
        self.para_npreg = npreg
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
        # create the parameter template
        self.para_template = self.create_para_template()
        self.para_borg = None
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
            pass
