
import json
import csv
import os
from typing import Dict, List

def transform_dict_v3(table_info):
    """
    Modifies the dictionary to map table names directly to the values contained in their columns.
    Assumes each table's details is a list of [column_name, column_type] lists.
    """
    transformed_dict = {}
    for table_name, columns in table_info.items():
        # Initialize a dictionary for this table's columns
        columns_dict = {}
        for column in columns:
            column_name, column_type = column
            # Example transformation, adjust according to your needs
            columns_dict[column_name] = {"type": column_type, "data": []}
        transformed_dict[table_name] = columns_dict
    return transformed_dict


def populate_dict_from_csv_v3(folder_path: str, data_dict: Dict) -> Dict:
    """
    Populates the dictionary with data from CSV files matching the table and column names.
    Updates the dictionary structure to include table names as primary keys.
    """
    for file in os.listdir(folder_path):
        table_name = file.replace('.csv', '')
        if table_name in data_dict:
            file_path = os.path.join(folder_path, file)
            with open(file_path, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    for column in data_dict[table_name]:
                        if column in row:
                            # Inside populate_dict_from_csv_v3, adjust the line causing the KeyError to match the new structure
                            data_dict[table_name][column]["data"].append(row[column])

    return data_dict

def dict_to_json(data_dict: Dict) -> str:
    """
    Converts a dictionary to a JSON string.
    """
    return json.dumps(data_dict, indent=4)

# carica il json con le informazioni sulle tabelle
table_info = json.load(open(r"C:\Users\alessandro.amatori\Desktop\script\functional_analysis\columns_per_table.json", 'r'))
transformed_dict_v3 = transform_dict_v3(table_info)
final_dict_v3 = populate_dict_from_csv_v3(r"C:\Users\alessandro.amatori\Desktop\nuovi_csv", transformed_dict_v3)
final_json = dict_to_json(final_dict_v3)

#salva il nuovo json
with open('new_json_file.json', 'w') as f:
    f.write(final_json)