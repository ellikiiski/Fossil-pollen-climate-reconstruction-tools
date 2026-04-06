"""
Harmonize pollen data under specified taxon names.
"""

from unidecode import unidecode
import re
from data_harmonization import harmonization_prep as prep
from data_writing import json_handler as json
from data_writing import excel_handler as excel

def harmonize(data_json_file_path, rules_file_path, harmonized_json_file_path, missing_json_file_path):
    """Harmonize the data of json file in data_json_file_path
    with the rule in rules_file_path (if the file is excel, first create rules json file)
    and write it into json file in harmonized_json_file_path."""

    rules = json.load_json(rules_file_path)
    data = json.load_json(data_json_file_path)

    missing = {}

    for site in data:

        datasetid = site['pollen']['datasetid']

        pollendata = site['pollen']['samples']
        for sample in pollendata:

            sampledata = sample['samples']
            updated_sampledata = {}
            for taxon in sampledata.keys():

                og_name = taxon.lower()
                harmonized_name = rules.get(og_name, og_name)
                if harmonized_name == og_name:
                    if og_name not in missing.keys():
                        missing[og_name] = []
                    if datasetid not in missing[og_name]:
                        missing[og_name].append(datasetid)

                if harmonized_name != 'NONE':

                    if harmonized_name not in updated_sampledata.keys():
                        updated_sampledata[harmonized_name] = 0

                    updated_sampledata[harmonized_name] += sampledata[taxon]

            sample['samples'] = updated_sampledata

    missing = prep.aplhapbetize(missing)

    json.write_json(data, harmonized_json_file_path)
    json.write_json(missing, missing_json_file_path)


def normalize(labels, harmonized_json_file_path, normalized_json_file_path):
    """Reads the harmonized data from harmonized_json_file_path and sorts it undes labels
    and normalizes the values (to add up to 1) and writes each dataset in an excel file."""
    
    data = json.load_json(harmonized_json_file_path)

    normalized_sites = []

    for site in data:

        siteid = site['siteid']
        sitename = site['sitename']
        pollendata = site['pollen']['samples']

        for sample in pollendata:

            sampledata = sample['samples']

            if sampledata != {}:
                normalized_samples = {}
                total = 0

                for label in labels:

                    if label in sampledata.keys():
                        value = sampledata[label]
                        normalized_samples[label] = value
                        total += value
                    else:
                        normalized_samples[label] = 0
                
                if total != 0:
                    for name, value in normalized_samples.items():
                        normalized_samples[name] = normalized_samples[name] / total
                else:
                    depth = sample['sampledepth']
                    print(f'WARING: Found a sample with no taxa from site: {sitename} ({siteid}) in depth {depth}.')

                sample['samples'] = normalized_samples
                site['filename'] = f'{clean_sitename(sitename)}_{siteid}'
        
        normalized_sites.append(site)

    json.write_json(normalized_sites, normalized_json_file_path)
        

def clean_sitename(sitename):
    sitename_clean1 = unidecode(sitename)
    sitename_clean2 = re.sub(r'[^A-Za-z]', '', sitename_clean1)
    return sitename_clean2