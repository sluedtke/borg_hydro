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
                                                  './config_schema.json')
    config_schema = read_json_file(schema_file)
    # Validate with the user configuration given
    jsonschema.validate(model_config, config_schema)


# --------------------------
class user_borg_model():
    '''
    A class that holds all the configs given by the json file. Not sure whether
    that is all a bit overkill, lets see
    '''
    def __init__(self, config_file):
        ''' Initialization of the model components.'''
        # Read json file
        config_data = read_json_file(config_file)
        # Validate the json schema. NOTE: the function only raises an error if
        # the validation fails.
        validate_config(config_data)
        # address project name
        self.pn = config_data['project_name']
        # address project path
        self.pp = config_data['project_path']
        # address result path
        self.rp = config_data['result_path']
        # --------------------------
        # get the parameter list and format it for borg
        self.para_names = [para['name'] for para in config_data['parameters']]
        # get parameter min and max
        parameter_min = [para['min'] for para in config_data['parameters']]
        parameter_max = [para['max'] for para in config_data['parameters']]
        self.parameter_range = list(map(list, zip(parameter_min,
                                   parameter_max)))
        # --------------------------
        # get the objectives as a list of dicts
        self.objectives = [objs for objs in config_data['objectives']]
