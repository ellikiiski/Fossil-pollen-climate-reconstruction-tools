"""
Filter sites (output by dataset_fetcher.py) by metrics of pollen data and chronologies
and create summary/info/metadata json file.

Filter functions: filter_by_pollendata and filter_by_chonologies
Summary function: summary (strips the sample data out of the file)
"""

from ..helpers import json_handler as json

# FUNCTIONS TO BE USED BY OTHER MODULES

def filter_sites(datasets_file_path, write_file_path, min_oldest=None, max_youngest=None, pollen_min_number=None, chrono_min_number=None):
    """Filters the json file in datasets_file_path by removing all sites,
    pollen data or chronologies  of which do not satisfy the requirements
    of given parameters."""

    data = json.load_json(datasets_file_path)
    
    filtered_by_chronologies = _chronology_filter(data, chrono_min_number, min_oldest, max_youngest)
    filtered_by_pollen = _pollen_sample_filter(filtered_by_chronologies, pollen_min_number)

    json.write_json(filtered_by_pollen, write_file_path)


def summary(datasets_file_path, summary_file_path):
    """Takes the data in json file in datasets_file_path,
    strips it from the sample data (laeving only sample metadata)
    and writes it into a json file in summary_file_path."""
    
    data = json.load_json(datasets_file_path)

    summarized = _strip_of_samples(data)

    json.write_json(summarized, summary_file_path)


# INTERNAL HELP FUNCTIONS BELOW

def _pollen_sample_filter(data, min_number=None):
    """Reads the json file in datasets_file_path and
    returns a dictionary containing all the sites,
    pollen data of which satisfies the requirements of given parameters."""

    accepted = []
        
    for site in data:
            
        number = site['pollen']['numberofsamples']

        number_ok = True

        # filtering
        if min_number != None and number < min_number:
            number_ok = False

        if number_ok:
            accepted.append(site)

    return accepted


def _chronology_filter(data, min_number=None, min_oldest=None, max_youngest=None):
    """Reads the json file in datasets_file_path and
    returns a dictionary containing all the sites,
    chronologies of which satisfies the requirements of given parameters."""

    accepted = []

    for site in data:
        
        number = site['chronologies']['numberofsamples']
        ageoldest = site['ageoldest']
        ageyoungest = site['ageyoungest']

        number_ok = True
        oldest_ok = True
        youngest_ok = True

        # filters
        if min_number != None and number < min_number:
            number_ok = False
        if ageoldest == None or (min_oldest != None and ageoldest < min_oldest):
            oldest_ok = False
        if ageyoungest == None or (max_youngest != None and ageyoungest > max_youngest):
            youngest_ok = False

        if number_ok and oldest_ok and youngest_ok:
            accepted.append(site)

    print(f' {len(accepted)} sites passed the filter.')

    return accepted


def _strip_of_samples(data):
    """Removes the sample data (both pollen and chronological) of the given data.
    Removes also the filename row."""

    for site in data:
        del site['filename']
        del site['pollen']['samples']
        del site['chronologies']['samples']

    return data