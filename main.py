import pandas as pd

# Local imports 
from paths import *
from regex import dateConverterHelper, tempDateParser, tempTimeParser

# Define dictionary of dataframe:files
datasets = {
    'chlorophyll' : 'chlorophyll.csv',
    'hab_events' : 'hab_events.csv',
    'hab_occurences' : 'hab_occurences.csv',
    'nutrients' : 'nutrients.csv',
    'o_fldc_pm' : 'o_fl_derived_chlorophyll.csv',
    'secchi' : 'secchi.csv',
    # 'surfacewater_temps' : 'surfacewater_temp.csv',
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
    hab_occurences = dataframe['hab_occurences']
    nutrients = dataframe['nutrients']
    o_fldc_pm = dataframe['o_fldc_pm']
    secchi = dataframe['secchi']
    # surfacewater_temps = dataframe['surfacewater_temps']
    temps = dataframe['temps']
    zooplankton = dataframe['zooplankton']

    
    # Cleaning data - Parse times and dates from sus formats
    hab_occurences['eventID'] = hab_occurences['eventID'].apply(dateConverterHelper)
    temps['date'] = temps['time'].apply(tempDateParser)
    # temps['time'] = temps['time'].apply(tempTimeParser) 
    
    
    # Cleaning data - Drop unnecessary columns
    
    unnamed_col = 'Unnamed: 0'
    
    chlorophyll = chlorophyll.drop(columns=[unnamed_col,'Station Name'])
    hab_events = hab_events.drop(columns=[unnamed_col,'eventID','countryCode','station','geodeticDatum','coordinateUncertaintyInMeters'])
    hab_occurences = hab_occurences.drop(columns=[unnamed_col,'ScientificNameID','occurrenceID','nameCode','basisOfRecord','organismQuantityType']) 
    nutrients = nutrients.drop(columns=[unnamed_col,'Station'])
    o_fldc_pm = o_fldc_pm.drop(columns=[unnamed_col,'Patrol','ID','station'])
    secchi = secchi.drop(columns=[unnamed_col,'Crew','Station Name','Schedule Date','Long_reported','Lat_reported','Comments','Counter Depth (ft)','Sounder Depth (ft)'])
    zooplankton = zooplankton.drop(columns=[unnamed_col,'region_name','Key','Station','PROJECT','Twilight','Net_Type','Pi','Mesh_Size(um)','Net_Mouth_Dia(m)','CTD'])
    temps = temps.drop(columns=[unnamed_col,'time','temperature_std_dev','salinity_std_dev'])
    
    
    # Cleaning data - Drop unnecessary rows
    o_fldc_pm = o_fldc_pm.drop(0)
    nutrients = nutrients.drop(0)
    temps = temps.drop(0)

    
    # Cleaning data - Rename columns
    chlorophyll = chlorophyll.rename(columns={'Date':'date', 'Time (UTC)':'time','lat_deg':'lat', 'long_deg':'lon'})
    hab_events = hab_events.rename(columns={'eventDate':'date', 'decimalLatitude':'lat', 'decimalLongitude':'lon'})
    hab_occurences = hab_occurences.rename(columns={'eventID':'date'})
    nutrients = nutrients.rename(columns={'latitude':'lat', 'longitude':'lon','no3':'nitrate', 'po4':'phosphate', 'si':'silicone'})
    secchi = secchi.rename(columns={'Date of Sample':'date','Time of Reading':'time','Latitude.(dd)':'lat','Longitude.(dd)':'lon'})
    temps = temps.rename(columns={'temperature':'temp','latitude':'lat','longitude':'lon'})
    zooplankton = zooplankton.rename(columns={'Date':'date', 'lon':'lon'})
    
    # Cleaning data - Sort the data
    chlorophyll = chlorophyll.sort_values(by=['date'])
    hab_events = hab_events.sort_values(by=['date'])

    # Cleaning data - convert to datetime
    chlorophyll['date'] = pd.to_datetime(chlorophyll['date'], errors='coerce')
    hab_events['date'] = pd.to_datetime(hab_events['date'], errors='coerce')
    hab_occurences['date'] = pd.to_datetime(hab_occurences['date'], errors='coerce')
    nutrients['date'] = pd.to_datetime(nutrients['date'], errors='coerce')
    o_fldc_pm['date'] = pd.to_datetime(o_fldc_pm['date'], errors='coerce')
    secchi['date'] = pd.to_datetime(secchi['date'], errors='coerce')
    zooplankton['date'] = pd.to_datetime(zooplankton['date'], errors='coerce')
    temps['date'] = pd.to_datetime(temps['date'], errors='coerce')
    
    
    # CLeaning data - converting values
    temps['salinity'] = temps['salinity'].apply(float)
    temps['temp'] = temps['temp'].apply(float)
    temps['lat'] = temps['lat'].apply(float)
    temps['lon'] = temps['lon'].apply(float)
    temps['depth'] = temps['depth'].apply(float)

    
    # CLeaning data - downsample

    temps = temps.groupby(['date'])[['salinity','temp','salinity_sample_count','temperature_sample_count','lat','lon','depth']].mean()
    
    
    # Convert to csv

    cleaned_datasets = {
    "hab_events.csv": hab_events,
    "hab_occurences.csv": hab_occurences,
    "chlorophyll.csv": chlorophyll,
    "nutrients.csv": nutrients,
    "o_fldc_pm.csv": o_fldc_pm,
    "secchi.csv": secchi,
    # "surfacewater_temps.csv": surfacewater_temps,
    "zooplankton.csv": zooplankton,
    "temps.csv": temps
}

    for filename, dataframe in cleaned_datasets.items():
        dataframe.to_csv(CLEAN_PATH / filename)
    
    
    # Print outputs
    # print('HA events:\n',hab_events)
    # print('HA occurences:\n:',hab_occurences)
    # print('chloropyll:\n',chloropyll)
    # print('nutrients:\n',nutrients)
    # print('oxygen and fluorine-derived chlorophyll:\n',o_fldc_pm)
    # print('secchi:\n',secchi)
    # print('surface water temperatures:\n',surfacewater_temps)
    # print('zooplankton:\n',zooplankton)
    # print('temp:\n',temp)
        

if __name__ == '__main__':
    main()