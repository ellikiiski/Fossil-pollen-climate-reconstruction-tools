"""
Functions for scripts.
To run the scripts, go to the scripts folder in the project root.
"""

import pollen_data_tools.constants as c
import pollen_data_tools.parameters as p
import pollen_data_tools.data_fetching.metadata_fetcher as meta
import pollen_data_tools.data_fetching.data_fetcher as data
import pollen_data_tools.data_fetching.data_filter as filt


## SCRIPT FUNCTIONS

def run_data_fetch():

    print(f'\nNEOTOMA TOOL FOR FETCHING AND FILTERING POLLEN DATA')

    # METADATA FETCHING
    if p.FETCH_STEP_1:
        print(f'\nSTEP 1: Fetching sites from Neotoma')
        _fetch_sites()
    else:
        print(f'\nSTEP 1 (Fetching sites from Neotoma) skipped.')

    # DATA FETCHING
    if p.FETCH_STEP_2:
        print(f'\nSTEP 2: Fetching data from Neotoma')
        _fetch_data()
    else:
        f'\nSTEP 2 (Fetching data from Neotoma) skipped.'

    # DATA FILTERING
    if p.FETCH_STEP_3:
        print(f'\nSTEP 3: Filtering sites')
        _filter_data()
    else:
        f'\nSTEP 3 (Filtering sites) skipped.'

    # EXCEL WRITING
    if p.FETCH_STEP_4:
        print(f'\nSTEP 4: Writing sites into Excel')
        #f.sites_excel_output()
    else:
        f'\nSTEP 4 (Writing sites into Excel) skipped.'

    print(f'\nDATA FETCHED AND SAVED SUCCESFULLY <3\n')


## INTERNAL HELP FUNCTIONS

# FETCH 1
def _fetch_sites():

    # text parameters for prints
    how_many = f'{p.MAX_SEARCHES} first' if p.MAX_SEARCHES != None else f'all'
    location_filter = p.COORDINATES if p.COORDINATES != None else f'not restricted'

    print(f'Fetching {how_many} pollen sites with coordinates {location_filter}.')

    # actual fetching of the sites
    meta.get_sites(c.METADATA_URL, c.DATASET_INFO_BASE_URL, c.SITES_FILE_PATH, p.COORDINATES, p.MAX_SEARCHES)

    print(f'\nSites fetched and written into json file in {c.SITES_FILE_PATH}.')

# FETCH 2
def _fetch_data():

    print(f'Fetching pollen data and chronologies of the sites listed in {c.SITES_FILE_PATH}.\n')

    data.fetch_datasets(c.DATASET_DOWNLOAD_BASE_URL, c.SITES_FILE_PATH, c.DATASETS_FILE_PATH)

    print(f'\nFull pollen and chronological data fetched and written in {c.DATASETS_FILE_PATH}.')

# FETCH 3
def _filter_data():

    # text parameters for prints
    pollen_number_filter = p.POLLEN_MIN_SAMPLES if p.POLLEN_MIN_SAMPLES != None else f'not restricted'
    chrono_number_filter = p.CHRONOLOGIES_MIN_SAMPLES if p.CHRONOLOGIES_MIN_SAMPLES != None else f'not restricted'

    print(f'Filtering the sites with the following restrictions:')
    print(f'...must cover age (upper): {p.MIN_OLDEST}')
    print(f'...must cover age (lower): {p.MAX_YOUNGEST}')
    print(f'...pollen data minimum number of samples: {pollen_number_filter}')
    print(f'...chronologies minumum number of samples: {chrono_number_filter}')

    filt.filter_sites(c.DATASETS_FILE_PATH, c.FILTERED_FILE_PATH, p.MIN_OLDEST, p.MAX_YOUNGEST, p.POLLEN_MIN_SAMPLES, p.CHRONOLOGIES_MIN_SAMPLES)
    filt.summary(c.FILTERED_FILE_PATH, c.SUMMARY_FILE_PATH)

    print(f'\nFiltered data written in {c.FILTERED_FILE_PATH}.')
    print(f'Summary of sites written in {c.SUMMARY_FILE_PATH}.')