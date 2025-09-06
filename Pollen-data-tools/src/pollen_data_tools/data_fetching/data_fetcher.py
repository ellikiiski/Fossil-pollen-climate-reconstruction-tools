"""
Fetch datasets from Neotoma dabase through the API.
Add pollen data samples and chronologies to existing metadata given as json file
(output from metadata_fetcher.py).
Function fetch_datasets writes a json file containing the full data of the sites.
"""

from ..helpers import json_handler as json
from ..helpers import api_requests as req


# FUNCTION TO BE USED BY OTHER MODULES
def fetch_datasets(base_url, sites_file_path, write_file_path):
    """Fetches the sample data of both pollen and chronologies from Neotoma,
    adds it among the site info and writes it into json file in write_file_path."""

    fetched_sites = _get_data(base_url, sites_file_path)

    json.write_json(fetched_sites, write_file_path)


# INTERNAL HELP FUNCTIONS BELOW

def _get_data(base_url, sites_file_path):
    """Goes through the (pollen and chronologies) dataset ids from sites_file_path,
    adds the sample data under corresponding data type (pollen or chronological)
    and returns the data as a dictionary."""

    sites = []

    data = json.load_json(sites_file_path)

    progress = 0
    total = len(data)

    print(f' Fetching data for {total} pollen sites...\n')

    # loop over sites and fetch both pollen and chronological datasets
    for site in data:

        pollen_id = site['pollen']['datasetid']
        chrono_id = site['chronologies']['datasetid']

        # fetch and save data as a dictionary
        pollendata = _get_pollen_samples(base_url, pollen_id)
        chronologies = _get_chronologies(base_url, chrono_id)

        if pollendata != None and chronologies != None:

            # save the number of samples
            numberofpollensamples = len(pollendata)
            numberofchronologies = len(chronologies)

            # determine age info
            (age_oldest, age_youngest) = _get_age_info(pollendata)

            # add number of samples and sample data into the site info
            site['ageoldest'] = age_oldest
            site['ageyoungest'] = age_youngest
            site['pollen']['numberofsamples'] = numberofpollensamples
            site['chronologies']['numberofsamples'] = numberofchronologies
            site['pollen']['samples'] = pollendata
            site['chronologies']['samples'] = chronologies

            sites.append(site)

            progress += 1 # update progress

            # print progress every 25 sites
            if progress % 25 == 0:
                print(f'  {progress}/{total} sites done...')
        
    return sites


def _get_pollen_samples(base_url, datasetid):
    """Fetches the data of given pollen dataset id from Neotoma
    and parses the relevant info and sample data into a dictionary.
    """
    
    data = req.fetch_dataset(base_url, datasetid)

    try:
        samples = data['data'][0]['samples']

        # loop over samples and parse relevant information
        pollen_data = []
        for sample in samples:

            # sample metadata
            depth = sample['analysisunitdepth']
            radiocarbon_age = None
            calibrated_radiocarbon_age = None
            # save age data if available
            age_data = sample['sampleages']
            for age in age_data:
                if age['agetype'] == 'Radiocarbon years BP':
                    radiocarbon_age = age['age']
                elif age['agetype'] == 'Calibrated radiocarbon years BP':
                    calibrated_radiocarbon_age = age['age']

            # create a sample info dictionary and save sample metadata
            sample_info = {}
            sample_info['sampledepth'] = depth
            sample_info['radiocarbonage'] = radiocarbon_age
            sample_info['age_calibrated'] = calibrated_radiocarbon_age
            # parse sample data
            sample_data = sample['sampledata']
            measurements = {}
            for data_point in sample_data: # form sample data into taxonname:value dictionary
                taxonname = data_point['taxonname']
                value = data_point['value']
                measurements[taxonname] = value
            # save sample data
            sample_info['samples'] = measurements
            pollen_data.append(sample_info)

        return pollen_data

    except:
        print(f'Failed to read the data with dataset id {datasetid} (pollen data)')
        return None


def _get_chronologies(base_url, datasetid):
    """Fetches the data of given chronologies dataset id from Neotoma
    and parses the relevant info and sample data into a dictionary.
    """

    data = req.fetch_dataset(base_url, datasetid)

    try:
        samples = data['data'][0]['samples']

        # save the sample data in a list
        chronologies = [sample['analysisunitdepth'] for sample in samples]

        return chronologies

    except:
        print(f'Failed to read the data with dataset id {datasetid} (chronologies)')
        return None
        

def _get_age_info(pollen_data):
    """Gets the age of the top and bottom most samples and
    returns it as a tuple."""

    return (pollen_data[-1]['age_calibrated'], pollen_data[0]['age_calibrated'])