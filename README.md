# Project Title

TODO: Add project description

# Directory Structure

TODO: Add directory structure

# Installation

This project assumes that the user already has python and is able to do pip installations.

Install dependencies:
```bash
pip install -r requirements.txt
```

# Usage
## After cloning the repository, run the following commands sequentially in the root of the directory:
Convert any raw data xlsx files to csv, or if it is already csv, rename it to something appropriate:
```bash
python convert_data.py
```
Clean the datasets, and get it ready for merging into a master dataset:
*Note: This will take a moment as the datasets are relatively large.*
```bash
python clean_data.py
```
Merge the data together to be used in the program:
```bash
python merge_data.py
```
