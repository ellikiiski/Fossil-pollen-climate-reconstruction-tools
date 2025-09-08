"""
Preparation for the data harmonization:
- Create rules json file from existing excel file
- List found taxon names and label them based on rules and guessing
"""

from ..helpers import json_handler as json
from ..helpers import excel_handler as excel


def prep_rules_json(rules_excel_file_path, rules_json_file_path, og_name_index, label_index):
    """Parses the excel in rules_ecxel_file_path and
    writes the original_name:taxon_name dinctionary
    into json file in rules_json_file_path."""

    rules = excel.excel_to_dict(rules_excel_file_path, og_name_index, label_index)

    json.write_json(rules, rules_json_file_path)


def list_taxonnames(sites_json_file_path, rules_json_file_path, taxonnames_json_file_path):
    """Goes through the json file in sites_json_file_path and
    labels them by matching and guessing based on the rules in rules_json_file_path.
    Writes the original name, label, reasoning, incidences and example dataset link
    into a json file in taxonnames_json_file_path."""
    
    taxonnames = list_instances(sites_json_file_path)
    rules = json.load_json(rules_json_file_path)

    listed = []
    matched = 0
    guessed = 0

    for taxon in taxonnames.keys():

        info = {
            'original' : taxon,
            'label' : 'no label',
            'reasoning' : 'no reasoning',
            'instances' : len(taxonnames[taxon]),
            'example' : taxonnames[taxon][0]
        }

        if taxon in rules.keys():
            info['label'] = rules[taxon]
            info['reasoning'] = f'Matched with existing harmonization rules. (0)'

            matched += 1

        else:
            guess = guess_label(taxon, rules)
            info['label'] = guess['guessed']
            info['reasoning'] = guess['reasoning']

            if guess['guessed'] != '???':
                guessed += 1

        listed.append(info)

    total = len(listed)
    print(f' Matched: {matched}/{total}')
    print(f' Guessed: {guessed}/{total}')
    print(f' Unlabeled: {total-matched-guessed}/{total}')

    json.write_json(listed, taxonnames_json_file_path)


def list_instances(sites_json_file_path):
    """Parses the json file in sites_json_file_path and
    counts the ocurring taxon names and returns them
    as an aplhabetized taxonname:count dictionary."""

    taxonnames = {}

    sites = json.load_json(sites_json_file_path)

    for site in sites:
        
        datasetid = site['pollen']['datasetid']
        pollensamples = site['pollen']['samples']

        for sample in pollensamples:

            sampledata = sample['samples']
            for taxon in sampledata:

                taxon = taxon.lower()

                if taxon not in taxonnames.keys():
                    taxonnames[taxon] = []

                if datasetid not in taxonnames[taxon]:
                    taxonnames[taxon].append(datasetid)
        
    return alphapbetize(taxonnames)


def guess_label(taxonname, rules):
    """Guesses a label for taxon name (original) based on the harmonization rule (rules).
    If a good guess can not be done, returns '???'."""

    guess = {
        'original' : taxonname,
        'guessed' : f'???',
        'reasoning' : f'Could not guess.'
    }

    for og_name, label in rules.items():

        og_name = og_name
        label = label
        taxonname = taxonname
        first_part = og_name.split('_')[0]
        
        if label.lower() in taxonname.lower():
            guess['guessed'] = label.upper()
            guess['reasoning'] = f'Has the substring {label}. (1)'
            return guess
        
        if og_name.lower() in taxonname.lower():
            guess['guessed'] = label.upper()
            guess['reasoning'] = f'Has the substring {og_name} (categorized as {label}). (2)'
            return guess
        
        elif len(first_part) >= 4 and first_part.lower() in taxonname.lower():
            guess['guessed'] = label.upper()
            guess['reasoning'] = f'Has the substring {first_part} ({og_name} categorized as {label}). (3)'
            return guess

    return guess


def alphapbetize(taxonname_dict):
    """Help funtion to aplphabetize a dictionary by keys."""

    return {key: taxonname_dict[key] for key in sorted(taxonname_dict)}