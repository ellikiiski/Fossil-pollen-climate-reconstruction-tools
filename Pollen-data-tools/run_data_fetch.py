"""
Run this python file and this file only.
Change the values in constants.py to run the desired steps with
the chosen constants.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import constants as c
import main_functions as f


def run():

    print(f'\nNEOTOMA TOOL FOR FETCHING AND FILTERING POLLEN DATA')

    # METADATA FETCHING
    if c.FETCH_STEP_1:
        print(f'\nSTEP 1: Fetching sites from Neotoma')
        f.sites_fetching()
    else:
        print(f'\nSTEP 1 (Fetching sites from Neotoma) skipped.')

    # DATA FETCHING
    if c.FETCH_STEP_2:
        print(f'\nSTEP 2: Fetching data from Neotoma')
        f.data_fetching()
    else:
        f'\nSTEP 2 (Fetching data from Neotoma) skipped.'

    # DATA FILTERING
    if c.FETCH_STEP_3:
        print(f'\nSTEP 3: Filtering sites')
        f.data_filtering()
    else:
        f'\nSTEP 3 (Filtering sites) skipped.'

    # EXCEL WRITING
    if c.FETCH_STEP_4:
        print(f'\nSTEP 4: Writing sites into Excel')
        f.sites_excel_output()
    else:
        f'\nSTEP 4 (Writing sites into Excel) skipped.'

    print(f'\nDATA FETCHED AND SAVED SUCCESFULLY <3\n')


if __name__ == "__main__":
    run()