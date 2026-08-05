import pandas as pd
import numpy as np

# Local imports 
from paths import *
from regex import hab_occurrencesStationParser, hab_occurrencesDateParser, tempDateParser, tempTimeParser, o_fldc_pmDateParser
from merge_datasets import merge_datasets


# Define dictionary of dataframe:files
datasets = {
    'chlorophyll' : 'chlorophyll.csv',
    'hab_events' : 'hab_events.csv',
    'hab_occurrences' : 'hab_occurrences.csv',
    'nutrients' : 'nutrients.csv',
    'o_fldc_pm' : 'o_fl_derived_chlorophyll.csv',
    'secchi' : 'secchi.csv',
    'zooplankton' : 'zooplankton.csv', 
    'temps' : 'temps.csv',
}

def main():

 # Convert to dataframes
    dataframe = {
        dataframe : pd.read_csv(OUT_PATH / filename, na_values ='.')
        for dataframe, filename in datasets.items() 
    }
    
    # Rename dictionary ones to avoid constantly calling datasets[] - probably inefficient but saves time when typing...
    chlorophyll = dataframe['chlorophyll']
    hab_events = dataframe['hab_events']
    hab_occurrences = dataframe['hab_occurrences']
    nutrients = dataframe['nutrients']
    o_fldc_pm = dataframe['o_fldc_pm']
    secchi = dataframe['secchi']
    temps = dataframe['temps']
    zooplankton = dataframe['zooplankton']

    
    # Cleaning data - Parse dates and station names
    hab_occurrences['eventDate'] = hab_occurrences['eventID'].apply(hab_occurrencesDateParser)
    o_fldc_pm['date'] = o_fldc_pm['date'].apply(o_fldc_pmDateParser)
    temps['date'] = temps['time'].apply(tempDateParser)
    
    
    # Cleaning data - Drop unnecessary columns
    unnamed_col = 'Unnamed: 0'
    chlorophyll = chlorophyll.drop(columns=[unnamed_col,'fid','Time (UTC)'])
    hab_events = hab_events.drop(columns=[unnamed_col,'countryCode','geodeticDatum','coordinateUncertaintyInMeters'])
    hab_occurrences = hab_occurrences.drop(columns=[unnamed_col,'ScientificNameID','occurrenceID','nameCode','basisOfRecord','organismQuantityType','kingdom']) 
    nutrients = nutrients.drop(columns=[unnamed_col,'time'])
    o_fldc_pm = o_fldc_pm.drop(columns=[unnamed_col,'Patrol','ID','time'])
    secchi = secchi.drop(columns=[unnamed_col,'Time of Reading','Crew','Schedule Date','Long_reported','Lat_reported','Comments','Counter Depth (ft)','Sounder Depth (ft)'])
    temps = temps.drop(columns=[unnamed_col,'time','temperature_std_dev','salinity_std_dev'])
    zooplankton = zooplankton.drop(columns=[unnamed_col,'region_name','Key','PROJECT','Twilight','Net_Type','Pi','Mesh_Size(um)','Net_Mouth_Dia(m)','CTD','STN_TIME','NOTES'])
    

    # Cleaning data - Drop unnecessary rows
    o_fldc_pm = o_fldc_pm.drop(0)
    nutrients = nutrients.drop(0)
    temps = temps.drop(0)

if __name__ == '__main__':
    main()