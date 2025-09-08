"""
Run this python file to harmonize the pollen data.
Change the values in parameters.py to run the desired steps.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from pollen_data_tools.functions import run_data_harmonization

if __name__ == "__main__":
    run_data_harmonization()

