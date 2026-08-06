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
│   └── clean_merged_data.py    # Clean the merged dataset prior to data analysis
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

# Convert, clean, merge datasets, then clean again
This project assumes that the user has already cloned the repository and has pathed to the root of the project.
## Run the following commands sequentially:

*Note: Some datasets are large, so the following commands will take a moment. Thank you for your patience.*

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
Finally, clean the merged data for analysis:
```bash
python src/clean_merged_data.py
```

Once you have run these commands, ensure there are csv files in the ``data/cleaned/`` directory. ``merged.csv`` and ``merged_cleaned.csv`` are the most important.

# Data explanation
This is an explanation of the variables found in ``merged.csv``. Variable names will displayed similar to as they are after the cleaning done in ``main.py``. 
## "Shared" variables:
- ``date`` (UTC): The date of recording. Identical through all the dataset. 
- ``station``: The station in charge of recording the data. Non-identical through all the datasets (varies due to different latitudes and longitudes).
- ``lat`` (latitude) (deg): The y position of the recorded data.
- ``lon`` (longitude) (deg): The x position of the recorded data. 
- ``d_km``: The calculated distance between the data and the data being merged.

*Note: ``d_km`` is not present in hab_events.csv and hab_occurrences.csv because they do not merge on similar locations, thus not requiring the ``merge_datasets.py`` function which returns the variable. This is not too important because ``d_km`` is irrelevant to our objective.*

### From the hab_events.csv dataset:
- ``eventID`` : The station and date of the recorded data. It is used to merge onto ``hab_occurrences.csv`` dataset.
- ``max_depth`` (m): The maximum depth.

### From the hab_occurrences.csv dataset:
- ``ScientificName``: The name of the observed plankton.
- ``organismQuantity``: The quantity of the observed plankton.
- ``occurrenceStatus``: The absence/presence of the algae booms.

### From the chlorophyll.csv dataset:
- ``chlorophyll`` (µg/L): The amount of chlorophyll present.
- ``phaeopigment`` (µg/L): The amount of phaeopigment present.

### From the nutrients.csv dataset:
- ``depth`` (m): The depth of recording.
- ``nitrate`` (μM): The amount of nitrate present.
- ``phosphate`` (μM): The amount of phosphate present.
- ``silicon`` (μM): The amount of silicon present.

### From the o_fldc_pm.csv dataset:
- ``pressure`` (dBar): The pressure of water (1 dbar ≈ 1 m)
- ``depth`` (m): The depth of the recording.
- ``temp`` (°C): The temperature of the water.
- ``conductivity`` (S/m): The conductivity of the water.
- ``salinity`` (TEOS-10 g/kg): The salinity levels of the water.
- ``oxygen_sat`` (%): The oxygen saturation of the water.
- ``oxygen_con`` (μM): The oxygen concentration of the water.
- ``chlorophyll`` (mg/mg^3): The amount of chlorophyll present.

### From the secchi.csv dataset:
This dataset calculates how far light is able to penetrate the water. This is
- ``avg_depth``: The average between where it was lowered to a point where it completely vanishes, and where it was raised until it was visible again.

Many variables were dropped during the process of cleaning, but they can be further explored in ``data/outputs/``.


# References and Acknowledgements

TODO: Add any references, data acquisition, etc.