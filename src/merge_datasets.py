import pandas as pd
import numpy as np
import math
from sklearn.neighbors import BallTree


def merge_datasets(df1, df2, prefix, d_max=5):
    
    '''
    Join datasets together based on date and proximity 
    '''
    RAD = 6371  # in km

    df1 = df1.copy().reset_index(drop=True)
    df2 = df2.copy().reset_index(drop=True)
    
    
    # Convert dates to pd.date_time
    df1['date'] = pd.to_datetime(df1['date'], errors='coerce').dt.normalize()
    df2['date'] = pd.to_datetime(df2['date'], errors='coerce').dt.normalize()
    
    
    # Convert latitudes and longitudes to floats
    df1['lat'] = pd.to_numeric(df1['lat'], errors='coerce')
    df1['lon'] = pd.to_numeric(df1['lon'], errors='coerce')

    df2['lat'] = pd.to_numeric(df2['lat'], errors='coerce')
    df2['lon'] = pd.to_numeric(df2['lon'], errors='coerce')
    
    df1 = df1.dropna(subset=['lat', 'lon', 'date']).reset_index(drop=True)
    df2 = df2.dropna(subset=['lat', 'lon', 'date']).reset_index(drop=True)
    
    results = []
    
    # Match dates
    for date in df1['date'].unique():

        # Make copies of the dataframes
        new_df = df1[df1['date'] == date].copy().reset_index(drop=True)
        df2_date = df2[df2['date'] == date].copy().reset_index(drop=True)


        # Skip if df2 has no corresponding date
        if df2_date.empty: continue

    
        # Convert latitude and longitude to radians
        df1_lat_rads = new_df['lat'] * math.pi / 180
        df1_lon_rads = new_df['lon'] * math.pi / 180
        
        df2_lat_rads = df2_date['lat'] * math.pi / 180
        df2_lon_rads = df2_date['lon'] * math.pi / 180
        
        df1_coords = np.column_stack((df1_lat_rads, df1_lon_rads))
        df2_coords = np.column_stack((df2_lat_rads, df2_lon_rads))
        
        
        # Define the ball tree
        tree = BallTree(df2_coords, metric='haversine')
        
        
        # Find nearest point on the same date
        d, i = tree.query(df1_coords, k=1)
        
        
        # Convert to kilometres
        d_km = d[:, 0] * RAD


        # Match rows
        matched = df2_date.iloc[i[:, 0]].copy().reset_index(drop=True)
        matched['d_km'] = d_km
        
        
        # Keep only matches within d_max
        within_distance = matched['d_km'] <= d_max
        new_df = new_df.loc[within_distance].reset_index(drop=True)
        matched = matched.loc[within_distance].reset_index(drop=True)


        result = pd.concat([new_df, matched.add_prefix(prefix)], axis=1)
        results.append(result)
    
    if not results: return pd.DataFrame()
    
    return pd.concat(results, ignore_index=True)