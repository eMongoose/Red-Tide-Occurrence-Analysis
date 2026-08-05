import pandas as pd
import numpy as np

# Local imports 
from paths import *
from regex import hab_occurrencesStationParser, hab_occurrencesDateParser, o_fldc_pmDateParser
from merge_datasets import merge_datasets


datasets = {
    'chlorophyll' : 'chlorophyll.csv',
    'hab_events' : 'hab_events.csv',
    'hab_occurrences' : 'hab_occurrences.csv',
    'nutrients' : 'nutrients.csv',
    'o_fldc_pm' : 'o_fldc_pm.csv',
    'secchi' : 'secchi.csv',
}

def main():
    '''
    Merge together the data for future analysis
    '''
    
    # Convert to dataframes
    dataframe = {
        dataframe : pd.read_csv(CLEAN_PATH / filename, na_values ='.')
        for dataframe, filename in datasets.items() 
    }
    
    # Rename dictionary ones to avoid constantly calling datasets[] - probably inefficient but saves time when typing...
    chlorophyll = dataframe['chlorophyll']
    hab_events = dataframe['hab_events']
    hab_occurrences = dataframe['hab_occurrences']
    nutrients = dataframe['nutrients']
    o_fldc_pm = dataframe['o_fldc_pm']
    secchi = dataframe['secchi']
    
    d_max = 5
    
    
    # Merge hab_events and hab_occurrences
    merged = hab_events.merge(hab_occurrences, on='eventID', how='outer')
    print('events and occurrences: ', merged.shape)

    # Merge with chlorophyll, with a max distance of 5 km
    merged = merge_datasets(merged, chlorophyll, 'chl_', d_max)
    print('chlorophyll: ', merged.shape)

    # Merge nutrients
    merged = merge_datasets(merged, nutrients, 'nut_', d_max)
    print('nutrients: ', merged.shape)
    
    # Merge o_fldc_pm
    merged = merge_datasets(merged, o_fldc_pm, 'o_', d_max)
    print('o_fldc_pm: ', merged.shape)
    
    # Merge secchi
    merged = merge_datasets(merged, secchi, 'secchi_', d_max)
    print('secchi: ', merged.shape)
    
    # Output to CSV file
    merged.to_csv(CLEAN_PATH / 'merged.csv')
    
    
if __name__ == '__main__':
    main()