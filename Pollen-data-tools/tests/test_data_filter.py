"""
Tests for data_filter.py.
"""

from pollen_data_tools.data_fetching import data_filter as filt
from pollen_data_tools import constants as c
import json

with open('tests/test_data/test_datasets_1.json', 'r', encoding='utf-8') as file:
    data1 = json.load(file)

with open('tests/test_data/test_data_summary_1.json', 'r', encoding='utf-8') as file:
    data2 = json.load(file)


def test_strip_of_samples():
    assert filt._strip_of_samples(data1) == data2

def test_chronology_filter():

    test1 = filt._chronology_filter(data1, min_number=21, min_oldest=9099, max_youngest=19)
    test2 = filt._chronology_filter(data1, min_number=10, min_oldest=900, max_youngest=20)
    test3 = filt._chronology_filter(data1, min_number=30, min_oldest=9000, max_youngest=20)
    test4 = filt._chronology_filter(data1, min_number=10, min_oldest=10000, max_youngest=20)
    test5 = filt._chronology_filter(data1, min_number=10, min_oldest=9000, max_youngest=0)

    assert len(test1) == 1
    assert len(test2) == 1
    assert len(test3) == 0
    assert len(test4) == 0
    assert len(test5) == 0

def test_pollen_sample_filter():

    test1 = filt._pollen_sample_filter(data1, min_number=10)
    test2 = filt._pollen_sample_filter(data1, min_number=135)
    test3 = filt._pollen_sample_filter(data1, min_number=200)

    assert len(test1) == 1
    assert len(test2) == 1
    assert len(test3) == 0