#!/usr/bin/python
######################################################################

#       Filename: config.py

#       Author: Stefan Luedtke

######################################################################

import json
import jsonschema
import pkg_resources

######################################################################


# --------------------------
def read_json_file(json_file):
    '''
    Function to read a json file.
    '''
    with open(json_file) as json_file:
        json_data = json.load(json_file)
    return(json_data)


def validate_config(model_config):
    '''
    Function to validate the user model configuration with the required one.
    '''
    # Read the schema that is stored in this directory. This will be used to
    # validate the user given configuration.
    schema_file = pkg_resources.resource_filename(__name__,
                                                  'config_schema.json')
    config_schema = read_json_file(schema_file)
    # Validate with the user configuration given
    jsonschema.validate(model_config, config_schema)


# --------------------------
class swim_setup():
    '''
    A class that holds all the general configs given by the json file.
    '''
    def __init__(self, config_file):
        ''' Initialization of the model components.'''
        # Read json file
        config_data = read_json_file(config_file)
        # Validate the json schema. NOTE: the function only raises an error if
        # the validation fails.
        validate_config(config_data)
        # get the first slot that hold general setup data
        general = config_data['general']
        # address project name
        self.pn = general['project_name']
        # address project path
        self.pp = general['project_path']


# --------------------------
class swim_parameter():
    '''
    A class that holds all the parameter properties given by the json file.
    '''
    def __init__(self, config_file):
        ''' Initialization of the model components.'''
        # Read json file
        config_data = read_json_file(config_file)
        # Validate the json schema. NOTE: the function only raises an error if
        # the validation fails.
        validate_config(config_data)
        parameter = config_data['parameters']
        # --------------------------
        # get the parameter list and format it for borg
        self.para_names = [para['name'] for para in parameter['list']]
        # get parameter min and max
        parameter_min = [para['min'] for para in parameter['list']]
        parameter_max = [para['max'] for para in parameter['list']]
        self.para_range = list(map(list, zip(parameter_min, parameter_max)))
        self.npreg = parameter['parameter_region_id']
        self.parameter_file = parameter['parameter_file']


class swim_objectives():
    '''
    A class that holds all the properties of the objectives given by the json
    file.
    '''
    def __init__(self, config_file):
        ''' Initialization of the model components.'''
        # Read json file
        config_data = read_json_file(config_file)
        # Validate the json schema. NOTE: the function only raises an error if
        # the validation fails.
        validate_config(config_data)
        # --------------------------
        # get the objectives as a list of dicts
        self.objectives = list(objs for objs in
                               config_data['objectives']['list'])
