"""
Run this python file to list the taxa appearing in the data and label them for hamonization.
Change the values in parameters.py to run the desired steps.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from pollen_data_tools.functions import run_harmonization_prep

if __name__ == "__main__":
    run_harmonization_prep()

