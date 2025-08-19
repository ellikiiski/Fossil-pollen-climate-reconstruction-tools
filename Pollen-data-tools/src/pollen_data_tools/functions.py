"""
Functions for scripts.
To run the scripts, go to the scripts folder in the project root.
"""

import pollen_data_tools.constants as c
import pollen_data_tools.parameters as p
import pollen_data_tools.data_fetching.metadata_fetcher as meta


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
        #f.data_fetching()
    else:
        f'\nSTEP 2 (Fetching data from Neotoma) skipped.'

    # DATA FILTERING
    if p.FETCH_STEP_3:
        print(f'\nSTEP 3: Filtering sites')
        #f.data_filtering()
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