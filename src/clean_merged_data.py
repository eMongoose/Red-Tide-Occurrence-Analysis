import pandas as pd
import numpy as np

from src.paths import *


def main():
    # Call the 
    df = pd.read_csv(CLEAN_PATH / 'merged.csv', index_col=0)
     
    # Clean the data 
    
    # Drop unnecessary or repetitive columns
    df = df.drop(columns={
        'eventID','date','station','lat','lon',
        'chl_date','chl_station','chl_lat','chl_lon','chl_d_km',
        'nut_date','nut_station','nut_lat','nut_lon','nut_d_km',
        'o_date','o_station','o_lat','o_lon','o_d_km',
        'secchi_date','secchi_station','secchi_lat','secchi_lon','secchi_d_km'
    })
    
    # Rename the data
    df = df.rename(columns={'eventDate':'date',
                            # 'chl_chlorophyll':'chlorophyll',
                            'chl_phaeopigment' : 'phaeopigment',
                            # 'nut_depth' : ' depth',
                            'nut_nitrate' : 'nitrate', 
                            'nut_phosphate': 'phosphate',
                            'nut_silicone' : 'silicon',
                            'o_pressure' : ' pressure',
                            # 'o_depth' : 'depth',
                            'o_temperature' : 'temp',
                            'o_conductivity' : 'conductivity',
                            'o_salinity' : 'salinity',
                            'o_oxygen_sat' : 'oxygen_sat',
                            'o_oxygen_con' : 'oxygen_con',
                            # 'o_chlorophyll' : 'chlorophyll',
                            'secchi_avg_depth' : 'avg_depth'
                            })
        
    
    df.to_csv(CLEAN_PATH / 'merged_cleaned.csv')
     

if __name__ == '__main__':
    main()