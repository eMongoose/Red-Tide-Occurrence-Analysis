import pandas as pd
from paths import *


xlsx_files = {
    '2015-2023_Chlorophyll_240628_SGDC2.xlsx' : 'chlorophyll.csv',
    'CitSci_Nutrients_2015-2023.xlsx' : 'nutrients.csv',
    '2015-2023_Secchi_250327_Final.xlsx' : 'secchi.csv',
    'CTD_2015-2023_250327.xlsx' : 'o_fl_derived_chlorophyll.csv',
}


csv_files = {
    '2023_HarmfulAlgalBlooms_Event.csv' : 'hab_events.csv',
    '2023_HarmfulAlgalBlooms_occurence.csv' : 'hab_occurrences.csv',
}


def fileReader(filename_input, filename_output):
    '''Convert xlsx -> csv file'''
    df = pd.read_excel(filename_input)
    df.to_csv(filename_output)
    
    
def fileRenamer(filename_input, filename_output):
    '''
    Simply rename, if already csv file.
    Note: there's probably a more efficient way of doing this...
    '''
    df = pd.read_csv(filename_input)
    df.to_csv(filename_output)


def fileConverter():
    '''xlsx -> csv file conversion, or just re-name to a readable file name'''
    for input, output in xlsx_files.items(): 
        fileReader(RAW_PATH / input, OUT_PATH / output)
        print(f'Currently reading {input} into {output}. Please wait a moment...')
        
    for input, output in csv_files.items():
        fileRenamer(RAW_PATH / input, OUT_PATH / output)
        print(f'currently reading {input} into {output}. Please wait a moment...')



def main():
    fileConverter()
    print('Data conversion has completed.')
    

if __name__ == '__main__':
    main()