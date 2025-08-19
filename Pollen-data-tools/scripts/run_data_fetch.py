"""
Run this python file to fetch the data from Neotoma database.
Change the values in parameters.py to run the desired steps with
the chosen parameters.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from pollen_data_tools.functions import run_data_fetch 

if __name__ == "__main__":
    run_data_fetch()

