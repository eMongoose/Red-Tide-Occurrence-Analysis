import pandas as pd
import re

r_fp = 'data/raw/mdp/'
u_fp = 'data/outputs/mdp/uncleaned/'
c_fp = 'data/outputs/mdp/cleaned/'

# date_re = re.compile(r"^(\S+) - - \[\S+ [+-]\d+\] \"[A-Z]+ \S+ HTTP/\d\.\d\" \d+ (\d+)$")

# sample input : VC4-1-26-2015-0
date_re = re.compile(r"^(\S+)-(\d+)-(\d+)-(\d+)-0$")

def dateConverterHelper(date):
    match = date_re.match(date)
    if match:
        month = match.group(2)
        day = match.group(3) 
        year = match.group(4)
        return f"{year}-{month}-{day}"
    else:
        return None

def fileReaderHelper(filename_input, skiprows, filename_output):
    '''Convert xlsx -> csv file'''
    df = pd.read_excel(filename_input, skiprows=skiprows)
    df.to_csv(filename_output)
    
def file_converters():
    '''Put xlsx -> csv file conversions here to declutter main function'''
    # fileReaderHelper(r_fp + '2015-2019_SurfaceWaterTemperature_240628.xlsx',0,'data/outputs/mdp/surfacewater_temperature.csv')
    # fileReaderHelper(r_fp + '2015-2023_Chlorophyll_240628_SGDC2.xlsx',0,'data/outputs/mdp/chlorophyll.csv')
    # fileReaderHelper(r_fp + '2015-2023_Secchi_250327_Final.xlsx',0,'data/outputs/mdp/secchi.csv')
    # fileReaderHelper(r_fp + 'CitSci_Nutrients_2015-2023.xlsx',0,'data/outputs/mdp/nutrients.csv')
    # fileReaderHelper(r_fp + 'CTD_2015-2023_250327.xlsx',0,'data/outputs/mdp/o_fl_derived_chlorophyll_profile_measurements.csv')
    # fileReaderHelper(r_fp + 'PSF Cit Sci Data Analysis and Queries - Hierarchy by stage_2024-05-30.xlsx',0,'data/outputs/mdp/zooplankton.csv')
    pass

def main():
    # Convert to dataframes
    hab_events_u = pd.read_csv(u_fp + '2023_HarmfulAlgalBlooms_Event.csv') # Harmful Algal Events
    hab_occurences_u = pd.read_csv(u_fp +'2023_HarmfulAlgalBlooms_Occurence.csv') # Harmful Algal Occurences
    chloropyll_u = pd.read_csv(u_fp + 'chlorophyll.csv',index_col=0)
    nutrients_u= pd.read_csv(u_fp + 'nutrients.csv',index_col=0)  
    o_fldc_pm_u = pd.read_csv(u_fp + 'o_fl_derived_chlorophyll_profile_measurements.csv',index_col=0) # Oxygen and Fluorine-derived chlorophyll profile measurements
    secchi_u = pd.read_csv(u_fp + 'secchi.csv',index_col=0)
    surfacewater_temps_u = pd.read_csv(u_fp + 'surfacewater_temperature.csv',index_col=0)
    zooplankton_u = pd.read_csv(u_fp + 'zooplankton.csv',index_col=0)
    
    
    # Cleaning data - Drop unnecessary columns
    hab_events = hab_events_u.drop(columns=['eventID','countryCode','station','geodeticDatum','coordinateUncertaintyInMeters'])
    hab_occurences = hab_occurences_u.drop(columns=['ScientificNameID','occurrenceID','nameCode','basisOfRecord','organismQuantityType']) 
    chloropyll = chloropyll_u.drop(columns=['Station Name'])
    nutrients = nutrients_u.drop(columns=['Station'])
    o_fldc_pm = o_fldc_pm_u.drop(columns=['Patrol','ID','station'])
    secchi = secchi_u.drop(columns=['Crew','Station Name','Schedule Date','Long_reported','Lat_reported','Comments','Counter Depth (ft)','Sounder Depth (ft)'])
    surfacewater_temps = surfacewater_temps_u.drop(columns=['Station','Patrol','Season'])
    zooplankton = zooplankton_u.drop(columns=['region_name','Key','Station','PROJECT','Twilight','Net_Type','Pi','Mesh_Size(um)','Net_Mouth_Dia(m)','CTD'])
    
    # Cleaning data - Drop unnecessary rows
    o_fldc_pm = o_fldc_pm.drop(0)
    nutrients = nutrients.drop(0)


    # Cleaning data - Parse dates from sus formats
    hab_occurences['eventID'] = hab_occurences['eventID'].apply(dateConverterHelper)
    
    # Cleaning data - Rename columns
    hab_events = hab_events.rename(columns={'eventDate':'date', 'decimalLatitude':'lat', 'decimalLongitude':'long'})
    hab_occurences = hab_occurences.rename(columns={'eventID':'date'})
    chloropyll = chloropyll.rename(columns={'Date':'date', 'Time (UTC)':'time','lat_deg':'lat', 'long_deg':'long'})
    nutrients = nutrients.rename(columns={'latitude':'lat', 'longitude':'long','no3':'nitrate', 'po4':'phosphate', 'si':'silicone'})
    secchi = secchi.rename(columns={'Date of Sample':'date','Latitude.(dd)':'lat','Longitude.(dd)':'Longitude.(dd)'})
    zooplankton = zooplankton.rename(columns={'Date':'date', 'lon':'long'})
    
    # Cleaning data - Sort the data
    chloropyll = chloropyll.sort_values(by=['date'])
    
    
    # Convert to csv
    hab_events.to_csv(c_fp + 'hab_events.csv')
    hab_occurences.to_csv(c_fp + 'hab_occurences.csv')
    chloropyll.to_csv(c_fp + 'chloropyll.csv')
    nutrients.to_csv(c_fp + 'nutrients.csv')
    o_fldc_pm.to_csv(c_fp + 'o_fldc_pm.csv')
    secchi.to_csv(c_fp + 'secchi.csv')
    surfacewater_temps.to_csv(c_fp + 'surfacewater_temps.csv')
    zooplankton.to_csv(c_fp + 'zooplankton.csv')
    
    
    # Print outputs
    print('HA events:\n',hab_events)
    print('HA occurences:\n:',hab_occurences)
    print('chloropyll:\n',chloropyll)
    print('nutrients:\n',nutrients)
    print('oxygen and fluorine-derived chlorophyll:\n',o_fldc_pm)
    print('secchi:\n',secchi)
    print('surface water temperatures:\n',surfacewater_temps)
    print('zooplankton:\n',zooplankton)
        

if __name__ == '__main__':
    main()