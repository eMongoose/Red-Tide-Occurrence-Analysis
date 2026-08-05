def NaNDetector(df):
    total_nans = df.isna().sum()
    total_count = df.size
    
    print(f"NaN items: {total_nans}")
    print(f"Total items: {total_count}")
