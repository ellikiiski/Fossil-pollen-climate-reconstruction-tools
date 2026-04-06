"""
Read pollen data from a json file (normalized data listed per site)
and create new json file for each taxon,
where the data is given by location, sorted under desired age slots.
"""

import json


def prep_data(taxon, age_slots, data_json_file, output_json_folder):
    """Reads the data from data_json_file and gets the pollen samples and
    corresponding coordinates of given taxon and
    writes the findings under given age_slots in output_json_file."""

    try:
        with open(data_json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

    except FileNotFoundError:
        print(f"Error: File '{data_json_file}' not found.")
        return None

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in '{data_json_file}': {e}")
        return None

    output = prep_taxon(taxon, age_slots, data)

    output_json_file = f'{output_json_folder}/{taxon}.json'

    with open(output_json_file, 'w', encoding='utf-8') as json_file:
        json.dump(output, json_file, indent=4, ensure_ascii=False)


def prep_taxon(taxon, age_slots, data):
    '''For given taxon, goes through the data and
    assigns the pollen counts of each location under given age_slots
    and returns a normalized dictionary.'''

    output = prep_age_slots(age_slots)

    for site in data:

        latitude = site['latitude']
        longitude = site['longitude']
        coordinates = f'{latitude}, {longitude}'

        pollendata = site['pollen']['samples']

        for measurements in pollendata:

            age = measurements['age_calibrated']
            age_slot = get_age_slot(age, age_slots)

            samples = measurements['samples']
                
            if age_slot != None and taxon in samples.keys():
                    
                if coordinates not in output[age_slot].keys():
                    output[age_slot][coordinates] = [0, 0]
                    
                output[age_slot][coordinates][0] += samples[taxon]
                output[age_slot][coordinates][1] += 1

    return normalize(output)


def prep_age_slots(age_slots):
    """Returns a dictionary with the age_slots as keys."""

    output = {}

    for age_slot in age_slots[1:]:
        output[age_slot] = {}

    return output


def get_age_slot(age, age_slots):
    """Returns the age slot of given age."""

    if age < age_slots[0]:
        return None
    
    for age_slot in age_slots:
        if age < age_slot:
            return age_slot
    return None
    

def prep_all(taxa, age_slots, data_json_file, output_json_folder):
    """Goes through all the taxa in data_json_file and
    creates a prepped json file for each."""
    
    try:
        with open(data_json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

    except FileNotFoundError:
        print(f"Error: File '{data_json_file}' not found.")
        return None

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in '{data_json_file}': {e}")
        return None

    for taxon in taxa:

        output = prep_taxon(taxon, age_slots, data)
        output_json_file = f'{output_json_folder}/{taxon}.json'

        with open(output_json_file, 'w', encoding='utf-8') as json_file:
            json.dump(output, json_file, indent=4, ensure_ascii=False)


def normalize(data):

    output = {}

    for age, pollen in data.items():

        output[age] = {}

        for coordinates, samples in pollen.items():

            average = 0

            if samples[1] != 0:
                average = samples[0] / samples[1]

            output[age][coordinates] = average
    
    return output



if __name__ == '__main__':

    taxa = [
        "ABIES", "ACER", "AESCULUS", "ALNUS", "APIACEAE", "ARMERIA", "ARTEMISI", 
        "ASTERACE", "BETULA", "BORAGINA", "BRASSICA", "BUXUS", "CAMPANUL", 
        "CAPRIFOL", "CARYOPHY", "CASTANEA", "CHENOPOD", "CORNUS", "CORYLUS", 
        "CYPERACE", "DRYAS", "ELAEAGNA", "EPHEDRA", "EQUISETU", "ERICACEA", 
        "EUPHORBI", "FABACEAE", "FAGUS", "FRAXINUS", "JUGLANDA", "JUNIPERU", 
        "LAMIACEA", "LARIX", "LILIACEA", "LYCOPODI", "MALVACEA", "MYRICA_G", 
        "OLEA", "ONAGRACE", "OSTRYCAR", "PICEA", "PINUS", "PISTACIA", 
        "PLANTAGO", "PLATANUS", "POACEAE", "POLEMONI", "POLYGONA", 
        "POLYPODI", "POPULUS", "PTERIDIU", "QUER_DEC", "QUER_EVE", 
        "RANUNCUL", "RHAMNACE", "ROSACEAE", "RUBIACEA", "RUBUS", 
        "RUMEXOXY", "SALIX", "SANGUISO", "SAXIFRAG", "SCROPHUL", 
        "SELAGINE", "SPHAGNUM", "TAXUS", "THALICTR", "TILIA", 
        "ULMUS_ZE", "URTICACE"
    ]
    age_slots = [0, 2000, 4000, 6000, 8000, 10000, 11500]
    data_json_file = 'input/normalized.json'
    output_json_folder = 'data'

    prep_all(taxa, age_slots, data_json_file, output_json_folder)