import pandas as pd
from generator import EnsembleGenerator, PointSet 

def main():
    print("Starting program...")

    contacts = pd.read_csv('data/contacts_clean.csv', index_col=0)
    contact_orients = pd.read_csv('data/orientations_clean.csv')
    faults = pd.read_csv('data/faults.csv')
    fault_orients = pd.read_csv('data/fault_orientations.csv')
 
    generator = EnsembleGenerator(contacts, contact_orients, faults, fault_orients)

    # Create an ensemble and name it 'contacts' when prompted
    generator.generate_ensemble_uniform(original=generator.contacts, samples=10, error_gps=5)
    
    # Retrieve details on previously generated ensembles
    print()
    generator.get_ensemble_info()

    # Save ensemble dataframes as csvs by querying its name
    generator.save_ensemble_tocsv('contacts')

if __name__ == "__main__":
    main()