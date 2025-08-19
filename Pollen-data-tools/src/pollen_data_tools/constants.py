"""
Constants for database urls, taxon labels and file locations.
Do not change unless you know what you are doing!
"""

import os

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
# project root and folder paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
FILES_DIR = os.path.join(PROJECT_ROOT, 'files')
# json files
SITES_FILE_PATH = os.path.join(FILES_DIR, "sites.json")
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