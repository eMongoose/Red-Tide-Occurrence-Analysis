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

def NaNDetector(df):
    total_nans = df.isna().sum()
    total_count = df.size
    
    print(f"NaN items: {total_nans}")
    print(f"Total items: {total_count}")


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
    
    
    # Merge hab_events and hab_occurrences
    hab_merged = hab_events.merge(hab_occurrences, on='eventID', how='outer')
    hab_merged = hab_merged.drop(columns=['eventDate_y','eventID']) # Drop extra date column, and drop eventID
    
    
    # Cleaning data - Drop unnecessary rows
    o_fldc_pm = o_fldc_pm.drop(0)
    nutrients = nutrients.drop(0)
    temps = temps.drop(0)


    # Cleaning data - Rename columns
    chlorophyll = chlorophyll.rename(columns={'Date':'date','Station Name':'station','lat_deg':'lat', 'long_deg':'lon','chl (µg/L)':'chlorophyll','phaeo (µg/L)':'phaeopigment'})
    # hab_events = hab_events.rename(columns={'decimalLatitude':'lat', 'decimalLongitude':'lon'})
    # hab_occurrences = hab_occurrences.rename(columns={'eventID':'date'})
    hab_merged = hab_merged.rename(columns={'decimalLatitude':'lat', 'decimalLongitude':'lon', 'eventDate_x':'date','maximumDepthInMeters':'max_depth'})
    nutrients = nutrients.rename(columns={'latitude':'lat', 'longitude':'lon','no3':'nitrate', 'po4':'phosphate', 'si':'silicone','Station':'station'})
    o_fldc_pm = o_fldc_pm.rename(columns={'latitude':'lat', 'longitude':'lon','o2SAT':'oxygen_sat','o2uM':'oxygen_con','chl':'chlorophyll'})
    secchi = secchi.rename(columns={'Date of Sample':'date','Latitude.(dd)':'lat','Longitude.(dd)':'lon','Station Name':'station'})
    temps = temps.rename(columns={'temperature':'temp','latitude':'lat','longitude':'lon'})
    zooplankton = zooplankton.rename(columns={'Date':'date', 'lon':'lon','Station':'station'})
    
    
    # Cleaning data - Dropping data (explanation included)
    secchi = secchi.dropna(subset=['date']) # the missing data accounts for 0.36% of the data, with 8000+ entries. It will be ok without that bit.
    
    
    # Cleaning data - Filling missing lat and lon data with the most commonly occuring coordinate by station 
    chlorophyll['lat'] = chlorophyll.groupby('station')['lat'].transform(lambda x: x.fillna(x.mode()[0]))
    chlorophyll['lon'] = chlorophyll.groupby('station')['lon'].transform(lambda x: x.fillna(x.mode()[0]))
    hab_merged['lon'] = hab_merged.groupby('station')['lon'].transform(lambda x: x.fillna(x.mode()[0]))

    
    # Cleaning data - Convert dates to datetime
    chlorophyll['date'] = pd.to_datetime(chlorophyll['date'])
    hab_merged['date'] = pd.to_datetime(hab_merged['date'])
    nutrients['date'] = pd.to_datetime(nutrients['date'])
    o_fldc_pm['date'] = pd.to_datetime(o_fldc_pm['date'])
    secchi['date'] = pd.to_datetime(secchi['date'], errors='coerce')
    temps['date'] = pd.to_datetime(temps['date'])
    zooplankton['date'] = pd.to_datetime(zooplankton['date'])    
    

    # print(
    #     'chlorophyll:\n', chlorophyll.dtypes, '\n', 
    #     'hab_merged:\n', hab_merged.dtypes, '\n',
    #     'nutrients:\n', nutrients.dtypes, '\n',
    #     'o_fldc_pm:\n', o_fldc_pm.dtypes, '\n',
    #     'secchi:\n', secchi.dtypes, '\n',
    #     'temps:\n', temps.dtypes, '\n',
    #     'zooplankton:\n', zooplankton.dtypes)
    
    
    # Merging datasets - hab_merged with chlorophyll
    hab_c_merged = merge_datasets(hab_merged, chlorophyll, d_max=5)


    # NaNDetector(hab_c_merged)                      

    # Convert to csv

    cleaned_datasets = {
    "hab_events.csv": hab_events,
    "hab_occurrences.csv": hab_occurrences,
    'hab_merged.csv': hab_merged,
    "chlorophyll.csv": chlorophyll,
    "nutrients.csv": nutrients,
    "o_fldc_pm.csv": o_fldc_pm,
    "secchi.csv": secchi,
    # "surfacewater_temps.csv": surfacewater_temps,
    "zooplankton.csv": zooplankton,
    "temps.csv": temps,
    'hab_c_merged.csv': hab_c_merged
    }

    for filename, dataframe in cleaned_datasets.items():
        dataframe.to_csv(CLEAN_PATH / filename)
    
    
    # Print outputs
    # print('HA events:\n',hab_events)
    # print('HA occurrences:\n:',hab_occurrences)
    # print('chloropyll:\n',chloropyll)
    # print('nutrients:\n',nutrients)
    # print('oxygen and fluorine-derived chlorophyll:\n',o_fldc_pm)
    # print('secchi:\n',secchi)
    # print('surface water temperatures:\n',surfacewater_temps)
    # print('zooplankton:\n',zooplankton)
    # print('temp:\n',temp)
        

if __name__ == '__main__':
    main()