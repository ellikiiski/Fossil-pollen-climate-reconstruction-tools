"""
Tests for data_fetcher.py.
"""

from pollen_data_tools.data_fetching import data_fetcher as data
from pollen_data_tools import constants as c
import json

with open('tests/test_data/test_pollen_data_1.json', 'r', encoding='utf-8') as file:
    data1 = json.load(file)

def test_get_age_info():
    assert data._get_age_info(data1) == (10647, 16)