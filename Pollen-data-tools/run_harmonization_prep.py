"""
Run this python file to list the taxa appearing in the data and label them for hamonization.
Change the values in constants.py to run the desired steps and
define the files to be read from and written in.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import constants as c
import main_functions as f

def run():

    print(f'PREPAREMENT STEPS FOR THE DATA HARMONIZATION')

    # TRANSLATE RULES FROM EXCEL TO JSON
    if c.PREP_STEP_1:
        print(f'\nSTEP 1: Translating rules from excel to json')
        f.rules_json_prepping()
    else:
        print(f'\nSTEP 1 (Translating rules from excel to json) skipped.')

    # LABELING AND GUESSING LABELS
    if c.PREP_STEP_2:
        print(f'\nSTEP 2: Labeliing the taxa')
        f.labeling()
    else:
        f'\nSTEP 2 (Labeliing the taxa) skipped.'

    # DEXCEL WRITING
    if c.PREP_STEP_3:
        print(f'\nSTEP 3: Writing the taxa with labels into excel')
        f.taxon_label_excel_outuput()
    else:
        f'\nSTEP 3 (Writing the taxa with labels into excel) skipped.'

    print(f'\nHARMONIZATION PREP EXECUTED SUCCESSFULLY <3')


if __name__ == "__main__":
    run()