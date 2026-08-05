# Project Title

TODO: Add project description

# Directory Structure
```
├── data/
│   └── cleaned/
│   └── outputs/
│   └── raw/
├── src/
│   └── clean_data.py
│   └── convert_data.py
│   └── helper_functions.py
│   └── merge_data.py
│   └── merge_datasets.py
│   └── paths.py
│   └── regex.py
├── main.py
└── requirements.txt

```
# Installation

This project assumes that the user already has the python interpreter and is able to do pip installations.

Install required dependencies:
```bash
pip install -r requirements.txt
```

# Convert, clean, and merge datasets
## After cloning the repository, run the following commands sequentially in the root of the directory:

*Note: This will take a moment as the datasets are relatively large.*

Depending on how you installed python, you can call the interpreter with ``python`` or ``python3``

Convert any raw data xlsx files to csv, or if it is already csv, rename it to something appropriate:
```bash
python convert_data.py
```
Clean the datasets, and get it ready for merging into a master dataset:
```bash
python clean_data.py
```
Merge the data together to be used in the program:
```bash
python merge_data.py
```

Once you have run these three commands, ensure there are seven csv files in the ``data/cleaned/`` directory.
