import pandas as pd
import numpy as np

# Local imports 
from paths import *
from regex import hab_occurrencesStationParser, hab_occurrencesDateParser, o_fldc_pmDateParser


# Define dictionary of dataframe:files
datasets = {
    'chlorophyll' : 'chlorophyll.csv',
    'hab_events' : 'hab_events.csv',
    'hab_occurrences' : 'hab_occurrences.csv',
    'nutrients' : 'nutrients.csv',
    'o_fldc_pm' : 'o_fl_derived_chlorophyll.csv',
    'secchi' : 'secchi.csv',
}

def main():
    '''
    Clean data
    '''

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

    
    # Parse dates and station names
    hab_occurrences['date'] = hab_occurrences['eventID'].apply(hab_occurrencesDateParser)
    o_fldc_pm['date'] = o_fldc_pm['date'].apply(o_fldc_pmDateParser)
    
    
    # Drop unnecessary columns
    unnamed_col = 'Unnamed: 0'
    chlorophyll = chlorophyll.drop(columns=[unnamed_col,'fid','Time (UTC)'])
    hab_events = hab_events.drop(columns=[unnamed_col,'countryCode','geodeticDatum','coordinateUncertaintyInMeters'])
    hab_occurrences = hab_occurrences.drop(columns=[unnamed_col,'ScientificNameID','occurrenceID','nameCode','basisOfRecord','organismQuantityType','kingdom']) 
    nutrients = nutrients.drop(columns=[unnamed_col,'time'])
    o_fldc_pm = o_fldc_pm.drop(columns=[unnamed_col,'Patrol','ID','time'])
    secchi = secchi.drop(columns=[unnamed_col,'Time of Reading','Crew','Schedule Date','Long_reported','Lat_reported','Comments','Counter Depth (m)','Counter Depth (ft)','Sounder Depth (m)','Sounder Depth (ft)','Secchi Depth (m)','Secchi Depth (m).1'])
    

    # Drop unnecessary rows
    o_fldc_pm = o_fldc_pm.drop(0)
    nutrients = nutrients.drop(0)


    # Rename columns
    chlorophyll = chlorophyll.rename(columns={'Date':'date','Station Name':'station','lat_deg':'lat', 'long_deg':'lon','chl (µg/L)':'chlorophyll','phaeo (µg/L)':'phaeopigment'})
    hab_events = hab_events.rename(columns={'decimalLatitude':'lat', 'decimalLongitude':'lon','maximumDepthInMeters':'max_depth'})
    nutrients = nutrients.rename(columns={'latitude':'lat', 'longitude':'lon','no3':'nitrate', 'po4':'phosphate', 'si':'silicon','Station':'station'})
    o_fldc_pm = o_fldc_pm.rename(columns={'latitude':'lat', 'longitude':'lon','o2SAT':'oxygen_sat','o2uM':'oxygen_con','chl':'chlorophyll'})
    secchi = secchi.rename(columns={'Date of Sample':'date','Latitude.(dd)':'lat','Longitude.(dd)':'lon','Station Name':'station', 'Avg Depth (m)':'avg_depth'})


    # Dropping data
    secchi = secchi.dropna(subset=['date']) # the missing data accounts for 0.36% of the data, with 8000+ entries. It will be ok without that bit.
    
    
    # Filling missing lat and lon data with the most commonly occuring coordinate by station 
    chlorophyll['lat'] = chlorophyll.groupby('station')['lat'].transform(lambda x: x.fillna(x.mode()[0]))
    chlorophyll['lon'] = chlorophyll.groupby('station')['lon'].transform(lambda x: x.fillna(x.mode()[0]))
    hab_events['lon'] = hab_events.groupby('station')['lon'].transform(lambda x: x.fillna(x.mode()[0]))
    

    # Convert dates to datetime
    chlorophyll['date'] = pd.to_datetime(chlorophyll['date'])
    nutrients['date'] = pd.to_datetime(nutrients['date'])
    o_fldc_pm['date'] = pd.to_datetime(o_fldc_pm['date'])
    secchi['date'] = pd.to_datetime(secchi['date'], errors='coerce')
    
    
    # Convert depths to floats
    o_fldc_pm['depth'] = pd.to_numeric(o_fldc_pm['depth'], errors='coerce')
    nutrients['depth'] = pd.to_numeric(nutrients['depth'], errors='coerce')


    # Cap depth levels
    o_fldc_pm = o_fldc_pm[o_fldc_pm["depth"].between(0.5, 1.5)].copy()
    nutrients = nutrients[nutrients["depth"].between(0, 5)].copy()
    
    # print(
    #     'chlorophyll:\n', chlorophyll.dtypes, '\n', 
    #     'hab_merged:\n', hab_merged.dtypes, '\n',
    #     'nutrients:\n', nutrients.dtypes, '\n',
    #     'o_fldc_pm:\n', o_fldc_pm.dtypes, '\n',
    #     'secchi:\n', secchi.dtypes, '\n',
    # )

    
    # Output to CSV file
    cleaned_datasets = {
    "hab_events.csv": hab_events,
    "hab_occurrences.csv": hab_occurrences,
    "chlorophyll.csv": chlorophyll,
    "nutrients.csv": nutrients,
    "o_fldc_pm.csv": o_fldc_pm,
    "secchi.csv": secchi,
    }


    for filename, dataframe in cleaned_datasets.items():
        dataframe.to_csv(CLEAN_PATH / filename, index=False)    
        
    
    print('Cleaning data completed. Please check data/cleaned/ for the presence of CSV files to ensure the data has successfully been cleaned.')
    

if __name__ == '__main__':
    main()
