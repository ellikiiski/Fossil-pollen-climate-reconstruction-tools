"""
JSON reading and writing to prevent copy past code in other modules.
"""

import json


def load_json(json_file_path):
    """Load json file in json_file_path and return data as dictionary."""

    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found.")
        return None

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in '{json_file_path}': {e}")
        return None
    
    return data


def write_json(data, json_file_path):
    """Write data (dictionary) into jsnon file in json_file_path."""

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)