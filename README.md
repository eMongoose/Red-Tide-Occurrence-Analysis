# Project Title

TODO: Add project description

# Directory Structure
```
├── data/                       # The directories of data...
│   └── cleaned/                # ...after calling clean_data.py
│   └── outputs/                # ...after calling convert_data.py
│   └── raw/                    # ...in its original form, provided to the user.
│       └── ⋮
├── src/
│   └── clean_data.py           # Clean the datasets prior to merging together
│   └── convert_data.py         # Convert xlsx files to csv, or rename csv files 
│   └── helper_functions.py     # Helper functions for printing out helpful information
│   └── merge_data.py           # Call merge_datasets to merge datasets together
│   └── merge_datasets.py       # Ball tree with Haversine function to merge datasets on nearby data
│   └── paths.py                # Paths for calling/saving xlsx/csv files 
│   └── regex.py                # Parsing functions for data cleaning
├── main.py
└── requirements.txt            # All pip installation requirements

```
# Installation

This project assumes that the user already has a python interpreter and is able to do pip installations.

Install required dependencies:
```bash
pip install -r requirements.txt
```

# Convert, clean, and merge datasets
## After cloning the repository, run the following commands sequentially in the root of the directory:

*Note: Certain datasets are larger than others, so the following commands will take a moment. Thank you for your patience.*

Depending on how you installed python, ``python`` or ``python3`` are interchangeable.

Convert any raw data xlsx files to csv, or if it is already csv, rename it to something appropriate:
```bash
python src/convert_data.py
```
Clean the datasets, and get it ready for merging into a master dataset:
```bash
python src/clean_data.py
```
Merge the data together to be used in the program:
```bash
python src/merge_data.py
```

Once you have run these three commands, ensure there are csv files in the ``data/cleaned/`` directory. However, we will be working with the ``data/cleaned/merged.csv`` dataset.

# Data variables (merged.csv)
## "Shared" variables:
- ``date``: Identical through all the datasets
- ``station``: Non-identical through all the datasets (Will vary due to differing latitudes and longitudes)
- ``lat`` (latitude): The y position of the recorded data
- ``lon`` (longitude): The x position of the recorded data 
- ``d_km``: Calculated distance between the data and the data being merged

*Note: ``d_km`` is not present in hab_events.csv and hab_occurrences.csv because they do not merge on similar lat/lons, thus not requiring the ``merge_datasets.py`` function.*

### From the hab_events.csv dataset:
- ``eventID`` : Station and date, used to merge onto hab_occurrences.csv dataset
- ``max_depth``: Maximum depth in meters

### From the hab_occurrences.csv dataset:
- ``ScientificName``: The name of the observed plankton
- ``organismQuantity``: The quantity of the observed plankton
- ``occurrenceStatus``: The absence/presence of the algae booms

## From the chlorophyll.csv dataset:
- ``chlorophyll``:
- ``phaeopigment``:

## From the nutrients.csv dataset:
- ``depth``:
- ``nitrate``:
- ``phosphate``:
- ``silicone``:

## From the o_fldc_pm.csv dataset:
- ``pressure``:
- ``depth``:
- ``temperature``:
- ``conductivity``:
- ``salinity``:
- ``oxygen_sat``:
- ``oxygen_con``:
- ``chlorophyll``:

## From the secchi.csv dataset:
- ``avg_depth``:


# References and Acknowledgements

TODO: Add any references, data acquisition, etc.