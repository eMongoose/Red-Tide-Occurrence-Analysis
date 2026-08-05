import pandas as pd
import numpy as np
import math
from sklearn.neighbors import BallTree


def merge_datasets(df1, df2, d_max=5):
    
    '''
    Join datasets together based on proximity 
    '''
    RAD = 6371 # in km

    new_df = df1.reset_index(drop=True)    
    
    df1 = df1.copy().reset_index(drop=True)
    df2 = df2.copy().reset_index(drop=True)
    
    
    # Convert to float
    df1["lat"] = pd.to_numeric(df1["lat"], errors="coerce")
    df1["lon"] = pd.to_numeric(df1["lon"], errors="coerce")

    df2["lat"] = pd.to_numeric(df2["lat"], errors="coerce")
    df2["lon"] = pd.to_numeric(df2["lon"], errors="coerce")
    
    df1 = df1.dropna(subset=['lat','lon']).reset_index(drop=True)
    df2 = df2.dropna(subset=['lat','lon']).reset_index(drop=True)
    
    
    # Convert latitude to radians
    df1_lat_rads = df1["lat"] * math.pi / 180
    df1_lon_rads = df1["lon"] * math.pi / 180
    
    df2_lat_rads = df2["lat"] * math.pi / 180
    df2_lon_rads = df2["lon"] * math.pi / 180
    
    df1_coords = np.column_stack((df1_lat_rads, df1_lon_rads))
    df2_coords = np.column_stack((df2_lat_rads, df2_lon_rads))

    
    tree = BallTree(df2_coords, metric='haversine')
    
    
    # Find the nearest point
    d, i = tree.query(df1_coords, k=1)
    
    
    # Convert to kilometers
    d_km = d[:,0] * RAD


    # Match the rows
    matched = df2.iloc[i[:, 0]].copy().reset_index(drop=True)    
    matched['d_km'] = d_km
    
    
    # Drop groups too far apart
    within_distance = matched["d_km"] <= d_max

    new_df = new_df.loc[within_distance].reset_index(drop=True)
    matched = matched.loc[within_distance].reset_index(drop=True)

    
    result = pd.concat([new_df, matched.add_prefix('df2_')], axis=1)
    
    return result