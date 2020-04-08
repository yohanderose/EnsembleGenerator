# Ensemble generator class that coordinates data movement and operations in map2loop.
# Expected  functionality:
#     - Take in map2loop outputs and store original data
#     - Create Ensemble object with a name, timestamp and array of perturbed datasets
#     - Output these datasets as a named folder of csvs (for now) 

# TODO: 
#       - the actual perturbing functions (from mark)
#       - a docker container for development 
#       --> LoopProjectFile, think of design parent object
#       - separating out the program properly 
#       - check mem usage (or saving to disk) 
#       - create loop repo and restyle (https://www.python.org/dev/peps/pep-0008/)

import sys, os, shutil
from os import path
import time
import json

import numpy as np
import pandas as pd
import scipy.stats as ss

# this works but wants me to import all the packages listed in m2l_utils... not sure I want to do that.
from m2l_utils_egen import ddd2dircos # this import can be linked to m2l_utils once these functions are linked i.e. in the same or linked repos
from m2l_utils_egen import dircos2ddd # this import can be linked to m2l_utils once these functions are linked i.e. in the same or linked repos
from spherical_utils import sample_vMF # thanks to https://github.com/jasonlaska/spherecluster/
# from egen_func import sample_vMF
import m2l_utils_egen

class colours():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# 
class Ensemble():
    def __init__(self, name, timestamp, original, ensemble, params):
        super().__init__()
        self.name = name
        self.timestamp = timestamp
        self.original = original
        self.ensemble = ensemble
        self.params = params

# Object to handle all operations on and storage of the original data
# Holds a list of the original Ensemble followed by Ensembles of perturbed data
class EnsembleGenerator():
    # Initialise by passing the original dataframes into  
    def __init__(self, contacts, contact_orients, faults, fault_orients):
        # TODO: list of objects or loading functions 
        # - more than just dataframes, set different properties
        # - instantiate generator object with something else,
        super().__init__()
        self.contacts = contacts
        self.contact_orients = contact_orients
        self.faults = faults
        self.fault_orients = fault_orients       
        # [Ensemble, Ensemble, Ensemble ...]
        self.sets = []
        # TODO: name better


    # Helper function for tracking and retrieving many perturbed sets
    def get_ensemble_info(self):
        print('{:<14}'.format("name"), end='\t')
        print('{:<14}'.format("timestamp"), end='\t\t\t\t')
        print('{:<14}'.format("samples"))
        for Ensemble in self.sets:
            print('{:<14}'.format(Ensemble.name), end='\t')
            print('{:<14}'.format(time.ctime(Ensemble.timestamp)), end='\t\t')
            print('{:<14}'.format(len(Ensemble.ensemble)))
    
    # Search for an ensemble and output it perturbations to a folder
    def save_ensemble_toCSV(self, name):
        found = [set for set in self.sets if set.name == name]
        if found:
            name = found[0].name + "/"
            ensemble = found[0].ensemble
            original = found[0].original
            params = found[0].params

            try:
                # Currently overwrites existing dir!!
                if os.path.exists(name):
                    shutil.rmtree(name)
                os.makedirs(name)
                for m in range(len(ensemble)):
                    file_name = name + str(m) + ".csv"
                    ensemble[m].to_csv(file_name)

                # Save original
                file_name = name + "original" + ".csv"
                original.to_csv(file_name)
                
                # export params as text file
                with open(name + 'params.txt', 'w') as file:
                    file.write(json.dumps(params))

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(colours.FAIL + "ERROR:\t", exc_type, fname, exc_tb.tb_lineno, "" + colours.ENDC)
                return

    # samples is the number of draws, thus the number of models in the ensemble
    # error is the assumed error in the location, and will be the width of the distribution    
    # Stores these in a unique Ensemble object 
    def generate_ensemble(self, original, samples=10, distribution='uniform', error_gps=5, DEM=None):
        # TODO: Prevent duplicates if this is to be searched on

        name = input("What would you like to name this set?")
        timestamp = time.time()
        file_contacts = original.copy()
        ensemble = []
        params = {
            "samples" : samples,
            "distribution" : distribution,
            "error_gps" : error_gps,
            "DEM" : DEM
        }

##################################################################################################################################
        if distribution == 'uniform':
            # Do uniform sampling
            try:
                # DEM = # import DEM here for sample new elevations for surface elevations. ISSUE: Don't want to resample elevations for interfaces at depth. Depth constraints needs to be flagged as such?
                for m in range(0, samples):
                    new_coords_u = pd.DataFrame(np.zeros((len(file_contacts), 4)),
                                            columns=['X', 'Y', 'Z', 'formation'])  # uniform
                    
                    # VALUE ERROR print() break
                    for r in range(len(file_contacts)):
                        start_x = file_contacts.loc[r, 'X']
                        new_coords_u.loc[r, 'X'] = ss.uniform.rvs(size=1, loc=start_x-(error_gps/2), scale=error_gps)
                        start_y = file_contacts.loc[r, 'Y']
                        new_coords_u.loc[r, 'Y'] = ss.uniform.rvs(size=1, loc=start_y-(error_gps/2), scale=error_gps)
                        new_coords_u.loc[r, 'Z'] = file_contacts.loc[r, 'Z']  # placeholder for the moment
                        # TODO line to map new Z value based on sampling the DEM at the new X,Y location
                        new_coords_u.loc[r, 'formation'] = file_contacts.loc[r, 'formation']                  
                    
                    ensemble.append(new_coords_u)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(colours.FAIL + "ERROR:\t", exc_type, fname, exc_tb.tb_lineno, "" + colours.ENDC)
                return
        
        elif distribution == 'normal':
            # Do uniform sampling
            try:
                pass
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(colours.FAIL + "ERROR:\t", exc_type, fname, exc_tb.tb_lineno, "" + colours.ENDC)
                return
        elif distribution == 'vmf':
            pass
##################################################################################################################################
            
        newEnsemble = Ensemble(name, timestamp, original, ensemble, params)
        self.sets.append(newEnsemble)

        
            