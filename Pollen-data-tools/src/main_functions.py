"""
Main functions for running the program.
Change the filters and file paths and update urls in constants.py!
"""

import constants as c
import data_fetching.metadata_fetcher as meta
import data_fetching.dataset_fetcher as data
import data_fetching.dataset_filter as filt
import data_harmonization.harmonization_prep as prep
import data_harmonization.harmonizer as harm
import data_writing.data_writer as write


# FETCH 1
def sites_fetching():

    # text parameters for prints
    how_many = f'{c.MAX_SEARCHES} first' if c.MAX_SEARCHES != None else f'all'
    location_filter = c.COORDINATES if c.COORDINATES != None else f'not restricted'

    print(f'Fetching {how_many} pollen sites within coordinates {location_filter}.')

    # actual fetching of the sites
    meta.fetch_sites(c.METADATA_URL, c.DATASET_INFO_BASE_URL, c.SITES_FILE_PATH, c.COORDINATES, c.MAX_SEARCHES)

    print(f'\nSites fetched and written into json file in {c.SITES_FILE_PATH}.')


# FETCH 2
def data_fetching():

    print(f'Fetching pollen data and chronologies of the sites listed in {c.SITES_FILE_PATH}.\n')

    data.fetch_datasets(c.DATASET_DOWNLOAD_BASE_URL, c.SITES_FILE_PATH, c.DATASETS_FILE_PATH)

    print(f'\nFull pollen and chronological data fetched and written in {c.DATASETS_FILE_PATH}.')


# FETCH 3
def data_filtering():

    # text parameters for prints
    pollen_number_filter = c.POLLEN_MIN_SAMPLES if c.POLLEN_MIN_SAMPLES != None else f'not restricted'
    chrono_number_filter = c.CHRONOLOGIES_MIN_SAMPLES if c.CHRONOLOGIES_MIN_SAMPLES != None else f'not restricted'

    print(f'Filtering the sites with the following restrictions:')
    print(f'...must cover age (upper): {c.MIN_OLDEST}')
    print(f'...must cover age (lower): {c.MAX_YOUNGEST}')
    print(f'...pollen data minimum number of samples: {pollen_number_filter}')
    print(f'...chronologies minumum number of samples: {chrono_number_filter}')

    filt.filter_sites(c.DATASETS_FILE_PATH, c.FILTERED_FILE_PATH, c.MIN_OLDEST, c.MAX_YOUNGEST, c.POLLEN_MIN_SAMPLES, c.CHRONOLOGIES_MIN_SAMPLES)
    filt.summary(c.FILTERED_FILE_PATH, c.SUMMARY_FILE_PATH)

    print(f'\nFiltered data written in {c.FILTERED_FILE_PATH}.')
    print(f'Summary of sites written in {c.SUMMARY_FILE_PATH}.')


# FETCH 4
def sites_excel_output():

    print(f'Writing sites info into an excel file in {c.OUTPUT_EXCEL_FILE_PATH}.')

    write.write_sites_excel(c.FILTERED_FILE_PATH, c.OUTPUT_EXCEL_FILE_PATH)

    print(f'Sites saved in {c.OUTPUT_EXCEL_FILE_PATH}.')



# PREP 1
def rules_json_prepping():
    
    print(f'Reading harmonization rules from {c.EXCEL_HARMONIZATION_RULES_FILE_PATH}.')

    prep.prep_rules_json(c.EXCEL_HARMONIZATION_RULES_FILE_PATH, c.JSON_HARMONIZATION_RULES_FILE_PATH, c.RULES_KEY_INDEX, c.RULES_VALUE_INDEX)

    print(f'Rules written in {c.JSON_HARMONIZATION_RULES_FILE_PATH}.')


# PREP 2
def labeling():
    
    print(f'Listing taxon names from data in {c.DATA_TO_BE_HARMONIZED_FILE_PATH} and labeling them.')

    prep.list_taxonnames(c.DATA_TO_BE_HARMONIZED_FILE_PATH, c.JSON_HARMONIZATION_RULES_FILE_PATH, c.TAXON_LIST_FILE_PATH)

    print(f'Taxon names and given labels listed in {c.TAXON_LIST_FILE_PATH}.')


# PREP 3
def taxon_label_excel_outuput():

    print(f'Writing taxon labes from {c.TAXON_LIST_FILE_PATH} into an excel.')

    write.write_label_excel(c.TAXON_LIST_FILE_PATH, c.DATASET_DOWNLOAD_BASE_URL, c.EXCEL_HARMONIZATOIN_LABELS_FILE_PATH)

    print(f'Labels written in {c.EXCEL_HARMONIZATOIN_LABELS_FILE_PATH}.')



# HARM 1
def harmonizing():

    print(f'Replacing taxon names in {c.DATA_TO_BE_HARMONIZED_FILE_PATH} with labes in {c.HARMONIZATION_RULES_UPDATED_FILE_PATH}')

    harm.harmonize(c.DATA_TO_BE_HARMONIZED_FILE_PATH, c.HARMONIZATION_RULES_UPDATED_FILE_PATH, c.HARMONIZED_DATA_FILE_PATH, c.MISSING_LABELS_FILE_PATH)

    print(f'Harmonized data written in {c.HARMONIZED_DATA_FILE_PATH}.')
    print(f'Missing labels written in {c.MISSING_LABELS_FILE_PATH}.')


# HARM 2
def normalizing():

    print(f'Normalizing the harmonized data in {c.HARMONIZED_DATA_FILE_PATH}.')
    print(f'NOTE: For this step to be executed correctly, the data must be properly harmonized!')

    harm.normalize(c.HARMONIZED_LABELS, c.HARMONIZED_DATA_FILE_PATH, c.NORMALIZED_JSON_FILE_PATH)

    print(f'Normalized data written in {c.HARMONIZED_DATA_FILE_PATH}.')


# HARM 3
def dataset_excels_output():

    print(f'Writing harmonized and normalized datasets in {c.HARMONIZED_DATASET_EXCEL_FOLDER}')

    write.write_harmonized_dataset_excels(c.NORMALIZED_JSON_FILE_PATH, c.HARMONIZED_DATASET_EXCEL_FOLDER)