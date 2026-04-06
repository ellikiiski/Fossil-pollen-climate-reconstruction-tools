"""
Constants for database urls, file locations and filters.
This is the place to change the values for the run!
"""

## DATABASE URLS
METADATA_URL = 'https://api.neotomadb.org/v2.0/data/sites'
DATASET_INFO_BASE_URL = 'https://api.neotomadb.org/v1.5/data/datasets'
DATASET_DOWNLOAD_BASE_URL = 'https://api.neotomadb.org/v1.5/data/downloads'

## TAXON LABELS
HARMONIZED_LABELS = [
    "ABIES", "ACER", "AESCULUS", "ALNUS", "APIACEAE", "ARMERIA", "ARTEMISI", 
    "ASTERACE", "BETULA", "BORAGINA", "BRASSICA", "BUXUS", "CAMPANUL", 
    "CAPRIFOL", "CARYOPHY", "CASTANEA", "CHENOPOD", "CORNUS", "CORYLUS", 
    "CYPERACE", "DRYAS", "ELAEAGNA", "EPHEDRA", "EQUISETU", "ERICACEA", 
    "EUPHORBI", "FABACEAE", "FAGUS", "FRAXINUS", "JUGLANDA", "JUNIPERU", 
    "LAMIACEA", "LARIX", "LILIACEA", "LYCOPODI", "MALVACEA", "MYRICA_G", 
    "OLEA", "ONAGRACE", "OSTRYCAR", "PICEA", "PINUS", "PISTACIA", 
    "PLANTAGO", "PLATANUS", "POACEAE", "POLEMONI", "POLYGONA", 
    "POLYPODI", "POPULUS", "PTERIDIU", "QUER_DEC", "QUER_EVE", 
    "RANUNCUL", "RHAMNACE", "ROSACEAE", "RUBIACEA", "RUBUS", 
    "RUMEXOXY", "SALIX", "SANGUISO", "SAXIFRAG", "SCROPHUL", 
    "SELAGINE", "SPHAGNUM", "TAXUS", "THALICTR", "TILIA", 
    "ULMUS_ZE", "URTICACE"
]

## DATA FETCHING FILE PATHS
# json files
SITES_FILE_PATH = 'input/SITES.json'
DATASETS_FILE_PATH = 'output/json/datasets.json'
FILTERED_FILE_PATH = 'output/json/FILTERED.json'
SUMMARY_FILE_PATH = 'output/json/summary.json'
# excel files
OUTPUT_EXCEL_FILE_PATH = 'output/excel/SITES.xlsx'

## HARMONIZATION PREP FILE PATHS
# json files
JSON_HARMONIZATION_RULES_FILE_PATH = 'output/json/rules-final.json'
DATA_TO_BE_HARMONIZED_FILE_PATH = 'input/picked_datasets.json'
TAXON_LIST_FILE_PATH = 'output/json/taxonnames.json'
# excel files
EXCEL_HARMONIZATION_RULES_FILE_PATH = 'input/Harmonization_rules_final.xlsx'
EXCEL_HARMONIZATOIN_LABELS_FILE_PATH = 'output/excel/Harmonization_labels.xlsx'
# column indices in harmonization rules excel (starts from zero)
RULES_KEY_INDEX = 0     # column number of the original name
RULES_VALUE_INDEX = 3   # column number of the label

## DATA HARMONIZATION FILE PATHS
# json files
HARMONIZATION_RULES_UPDATED_FILE_PATH = JSON_HARMONIZATION_RULES_FILE_PATH
HARMONIZED_DATA_FILE_PATH = 'output/json/harmonized.json'
MISSING_LABELS_FILE_PATH = 'output/json/missing.json'
NORMALIZED_JSON_FILE_PATH = 'output/json/normalized.json'
# excel files
HARMONIZED_DATASET_EXCEL_FOLDER = 'output/excel/datasets/'

## FILTERS | Use None for no limit
# metadata
COORDINATES = [47.5, 90, -12, 67.5] # [min_latitude, max_latitude, min_longitude, max_longitude]
MAX_SEARCHES = None                 # Max number of sites to be fetched (mainly for testing)
# chronologies
CHRONOLOGIES_MIN_SAMPLES = 5        # Min number of chronologies in acceptable site
MIN_OLDEST = 10000                  # Min oldest aging of accepted site
MAX_YOUNGEST = 2000                 # Max youngest aging of accepted site
# pollen data
POLLEN_MIN_SAMPLES = 30             # Min number of polen samples in acceptable site

## RUN DATASET FETCH | which steps to run
FETCH_STEP_1 = True # Fetch sites within COORDINATES from Neotoma and save to SITES_FILE_PATH
FETCH_STEP_2 = True # Fetch data of site in SITES_FILE_PATH and save to DATASETS_FILE_PATH
FETCH_STEP_3 = True # Filter data in DATASETS_FILE_PATH based on filters above and save into FILTERED_FILE_PATH and SUMMARY_FILE_PATH
FETCH_STEP_4 = True # Write the list of sites from FILTERED_FILE_PATH into excel in OUTPUT_EXCEL_FILE_PATH

## RUN HARMONIZATION PREP
PREP_STEP_1 = True  # Read harmonization rules from EXCEL_HARMONIZATION_RULES_FILE_PATH and save to JSON_HARMONIZATION_RULES_FILE_PATH
PREP_STEP_2 = True  # List taxa from DATA_TO_BE_HARMONIZED_FILE_PATH and determine/guess labels based on JSON_HARMONIZATION_RULES_FILE_PATH and write decisions to TAXON_LIST_FILE_PATH
PREP_STEP_3 = True  # Write harmonization labes from TAXON_LIST_FILE_PATH to EXCEL_HARMONIZATOIN_LABELS_FILE_PATH

## RUN DATA HARMONIZATION
HARM_STEP_1 = True  # Replace the taxon names in DATA_TO_BE_HARMONIZED_FILE_PATH with labels in JSON_HARMONIZATION_RULES_UPDATED_FILE_PATH
                    # and write output results in HARMONIZED_DATA_FILE_PATH and MISSING_LABELS_FILE_PATH (also remove the ones labeled NONE)
HARM_STEP_2 = True  # Normalize harmonized data from HARMONIZED_DATA_FILE_PATH and write into NORMALIZED_DATA_FILE_PATH
HARM_STEP_3 = True  # Write harmonized data into separate excels