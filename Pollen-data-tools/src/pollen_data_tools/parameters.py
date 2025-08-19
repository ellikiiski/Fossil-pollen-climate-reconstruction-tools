"""
Parameters for filters and selecting which steps to run.
This is the place to change the values before the run!
"""

## FOR TESTING
MAX_SEARCHES = 1    # Max number of sites to be fetched (small number for a quick run through, None to get all the results)

## FILTERS | Use None for no limit
# metadata
COORDINATES = [47.5, 90, -12, 67.5] # [min_latitude, max_latitude, min_longitude, max_longitude]
# chronologies
CHRONOLOGIES_MIN_SAMPLES = 5        # Min number of chronologies in acceptable site
MIN_OLDEST = 10000                  # Min oldest aging of accepted site
MAX_YOUNGEST = 2000                 # Max youngest aging of accepted site
# pollen data
POLLEN_MIN_SAMPLES = 30             # Min number of polen samples in acceptable site

## RUN DATASET FETCH | which steps to run
FETCH_STEP_1 = True # Fetch sites within COORDINATES from Neotoma and save to SITES_FILE_PATH
FETCH_STEP_2 = False # Fetch data of site in SITES_FILE_PATH and save to DATASETS_FILE_PATH
FETCH_STEP_3 = False # Filter data in DATASETS_FILE_PATH based on filters above and save into FILTERED_FILE_PATH and SUMMARY_FILE_PATH
FETCH_STEP_4 = False # Write the list of sites from FILTERED_FILE_PATH into excel in OUTPUT_EXCEL_FILE_PATH

# ## RUN HARMONIZATION PREP
# PREP_STEP_1 = True  # Read harmonization rules from EXCEL_HARMONIZATION_RULES_FILE_PATH and save to JSON_HARMONIZATION_RULES_FILE_PATH
# PREP_STEP_2 = True  # List taxa from DATA_TO_BE_HARMONIZED_FILE_PATH and determine/guess labels based on JSON_HARMONIZATION_RULES_FILE_PATH and write decisions to TAXON_LIST_FILE_PATH
# PREP_STEP_3 = True  # Write harmonization labes from TAXON_LIST_FILE_PATH to EXCEL_HARMONIZATOIN_LABELS_FILE_PATH

# ## RUN DATA HARMONIZATION
# HARM_STEP_1 = True  # Replace the taxon names in DATA_TO_BE_HARMONIZED_FILE_PATH with labels in JSON_HARMONIZATION_RULES_UPDATED_FILE_PATH
#                     # and write output results in HARMONIZED_DATA_FILE_PATH and MISSING_LABELS_FILE_PATH (also remove the ones labeled NONE)
# HARM_STEP_2 = True  # Normalize harmonized data from HARMONIZED_DATA_FILE_PATH and write into NORMALIZED_DATA_FILE_PATH
# HARM_STEP_3 = True  # Write harmonized data into separate excels