"""
Tests for metadata_fetcher.py.
"""

from pollen_data_tools.data_fetching import metadata_fetcher as meta
from pollen_data_tools import constants as c
import json

dict1 = {123: 22, 666: 1, 69: 42}
dict2 = {123: 222, 69: 420, 777: 123}
dict3 = {123: [22, 222], 69: [42, 420]}
dict4 = {20: [20, 7867]}

with open('tests/test_data/test_site_data_1.json', 'r', encoding='utf-8') as file:
    data1 = json.load(file)

with open('tests/test_data/test_site_data_2.json', 'r', encoding='utf-8') as file:
    data2 = json.load(file)

def test_combine_ids():
    assert meta._combine_ids(dict1, dict2) == dict3

def test_location_check():
    assert meta._location_check(data1, [47.5, 90, -12, 67.5])
    assert meta._location_check(data1, [47.5, 50, -12, 67.5]) == False
    assert meta._location_check(data2, [47.5, 90, -12, 67.5]) == False
    assert meta._location_check(data2, [47.5, 50, -12, 67.5]) == False

def test_get_site_infos():
    result = meta._get_site_infos(dict4, c.DATASET_INFO_BASE_URL)
    site = result[0]
    assert site['siteid'] == 20
    assert site['sitename'] == 'Akuvaara'
    assert site['latitude'] == 69.12326
    assert site['longitude'] == 27.67406
    assert site['ageoldest'] == None
    assert site['ageyoungest'] == None
    assert site['pollen']['datasetid'] == 20
    assert site['chronologies']['datasetid'] == 7867