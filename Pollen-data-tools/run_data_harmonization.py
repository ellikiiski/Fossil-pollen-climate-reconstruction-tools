"""
Run this python file to harmonize the pollen data.
Change the values in constants.py to run the desired steps and
define the files to be read from and written in.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import constants as c
import main_functions as f

def run():

    print(f'POLLEN DATA HARMONIZATION')

    # HARMONIZE AND REMOVE NONES
    if c.HARM_STEP_1:
        print(f'\nSTEP 1: Harmonizing pollen data')
        f.harmonizing()
    else:
        print(f'\nSTEP 1 (Harmonizing pollen data) skipped.')

    # NORMALIZE
    if c.HARM_STEP_2:
        print(f'\nSTEP2: Normalizing the harmonized data')
        f.normalizing()
    else:
        print(f'STEP 2 (Normalizing the harmonized data) skipped.')

    # WRITE EXCELS
    if c.HARM_STEP_3:
        print(f'\nSTEP 3: Creating separate excels for harmonized datasets')
        f.dataset_excels_output()
    else:
        print(f'\nSTEP 3 (Creating separate excels for harmonized datasets) skipped.')

    print(f'\nDATA HARMONIZATION EXECUTED SUCCESSFULLY <3')


if __name__ == "__main__":
    run()