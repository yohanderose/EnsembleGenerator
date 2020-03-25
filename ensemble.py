# Ensemble generator class that coordinates data movement and operations in map2loop.
# Expected  functionality:
#     - Take in map2loop outputs and store original data
#     - Create PointSet object with a name, timestamp and array of perturbed datasets
#     - Output these datasets as a named folder of csvs (for now) 

import time
import pandas as pd

# Object that holds a **list of groups of dataframes**
        # sets = [[contact1, fault1, orient1],
        #        [contact2, fault2, orient2],
        #        [contact3, fault3, orient3]]
# This list changes depending on how many perturbations of the original 
# set are required by the user, keeps a name and timestamp for reference 
class PointSet():
    def __init__(self, name, timestamp, listOfSets):
        super().__init__()
        self.name = name
        self.timestamp = timestamp
        self.sets = listOfSets

# Object to handle all operations on and storage of the original data
# Holds a list of the original pointset followed by pointsets of perturbed data
class EnsembleGenerator():
    # Initialise by passing the original dataframes into  
    def __init__(self, *args):
        super().__init__()
        # [PointSet, PointSet, Pointset ...]
        self.pertub = []
        # So the original Pointset has data of length 1 (list of list of original)
        # Original set retrievable as a list at self.pertub[0].sets[0] 
        self.pertub.append(PointSet("Original", time.time(), [list(args)]))

    # Helper function for tracking and retrieving many perturbed sets
    def getAllSetInformation(self):
        print('{:<14}'.format("name"), end='\t')
        print('{:<14}'.format("time"), end='\t\t\t')
        print('{:<14}'.format("perturbations"))
        for pointset in self.pertub:
            print('{:<14}'.format(pointset.name), end='\t')
            print('{:<14}'.format(time.ctime(pointset.timestamp)), end='\t')
            # for s in pointset.sets:
            #     for df in s:
            #         print(df.head())
            print('{:<14}'.format(len(pointset.sets)))

    # Accepts number of perturbed sets to generate OR set by user
    # Stores these in Pointset object with unique (name, timestamp) 
    # Returns name and rough indication of pointset building and copying time
    def generatePerturbations(self):
        # TODO: Chuck a while loop here to disable duplicates 
        # and valid dir name checking/enforcing 
        name = input("What would you like to name this run? ")
        numSetsToGen = int(input("How many perturbed sets to generate? "))
        timestamp = time.time()
        # TODO: Do manipulations here
        # The following is dummy code that appends the original set 
        # as many times as specified to simulate the perturbed sets
        sets = []
        for i in range(numSetsToGen):
            sets.append(self.pertub[0].sets[0])

        self.pertub.append(PointSet(name, timestamp, sets))
        return name, time.time() - timestamp            

# Begin execution here
def main():
    print("Starting program...")

    # For now we can use the csvs in the local 'data' directory but later implement manual 
    # selection by the user
    contacts = pd.read_csv('data/contacts_clean.csv', index_col=0)
    contactOrientations = pd.read_csv('data/orientations_clean.csv')
    faults = pd.read_csv('data/faults.csv')
    faultOrientations = pd.read_csv('data/fault_orientations.csv')

    # Create generator object using original set of variable length
    generator = EnsembleGenerator(contacts, contactOrientations, faults, faultOrientations)
    
    # Test out creating a couple of different sized pointsets
    name, elapsed = generator.generatePerturbations()
    print(name, "created in", elapsed, "seconds.")
    print()
    name, duration = generator.generatePerturbations()
    print(name, "created in", elapsed, "seconds.")
    print()

    # Print out all existing pointset information
    generator.getAllSetInformation()

if __name__ == "__main__":
    main()

