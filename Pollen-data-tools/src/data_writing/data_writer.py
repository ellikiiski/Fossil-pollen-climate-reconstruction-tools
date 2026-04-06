"""
"""

import data_writing.json_handler as json
import data_writing.excel_handler as excel

def write_sites_excel(json_file_path, excel_file_path):
    """Write sites info from json in json_file_path into
    excel file in excel_file_path."""

    data = json.load_json(json_file_path)

    rows = []
    for item in data:
        row = {
            'Site id': item.get('siteid'),
            'Site name': item.get('sitename'),
            'Latitude': item.get('latitude'),
            'Longitude': item.get('longitude'),
            'Age oldest': item.get('ageoldest'),
            'Age youngest': item.get('ageyoungest'),
            'Pollen samples': item.get('pollen', {}).get('numberofsamples'),
            'Chronologies': item.get('chronologies', {}).get('numberofsamples')
        }

        rows.append(row)

    excel.write_excel(rows, excel_file_path)


def write_label_excel(json_file_path, base_url, excel_file_path):
    """Write labeling from json in json_file_path into
    excel file in excel_file_path."""
    
    data = json.load_json(json_file_path)

    rows = []
    for item in data:
        example_dataset = item.get('example')
        row = {
            'Original name': item.get('original'),
            'Instances': item.get('instances'),
            'Label': item.get('label'),
            'Reasoning': item.get('reasoning'),
            'Example dataset': f'{base_url}/{example_dataset}'
        }

        rows.append(row)

    excel.write_excel(rows, excel_file_path)


def write_harmonized_dataset_excels(normalized_json_file_path, harmonized_dataset_base_file_path_base):
    """Reads the harmonized data from harmonized_json_file_path and sorts it undes labels
    and normalizes the values (to add up to 1) and writes each dataset in an excel file."""
    
    data = json.load_json(normalized_json_file_path)

    for site in data:

        rows = []

        filename = site['filename']
        pollendata = site['pollen']['samples']

        for sample in pollendata:

            age = sample['age_calibrated']
            sampledata = sample['samples']

            row = {}
            row['Age_cal_a'] = age
            row.update(sampledata)

            rows.append(row)

            full_path = f'{harmonized_dataset_base_file_path_base}{filename}.xlsx'

            #print(full_path)
        
        excel.write_excel(rows, full_path)
        
