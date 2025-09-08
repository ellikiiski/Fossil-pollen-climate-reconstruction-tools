"""
Read and write excels.
"""

import pandas as pd


def excel_to_dict(excel_file_path, key_index, value_index):
    """Read excel and return dictionary."""

    data = pd.read_excel(excel_file_path, engine='openpyxl')

    dictionary = {}

    for index, row in data.iterrows():
        
        dict_key = row.iloc[key_index].lower()
        dict_value = row.iloc[value_index]

        dictionary[dict_key] = dict_value

    return dictionary


def write_excel(rows, excel_file_path):
    """Writes rows dictionary (key: column name, value: cell value)
    into an excel file in excel_file_path."""

    data = pd.DataFrame(rows)

    data.to_excel(excel_file_path, index=False)