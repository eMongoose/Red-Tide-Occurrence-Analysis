import pandas as pd
import numpy as np

# Local imports 
from src.paths import *
from src.regex import hab_occurrencesStationParser, hab_occurrencesDateParser, o_fldc_pmDateParser



def main():
    # Call the 
    df = pd.read_csv(CLEAN_PATH / 'merged.csv')
     
    # Clean the data 
     
        

if __name__ == '__main__':
    main()