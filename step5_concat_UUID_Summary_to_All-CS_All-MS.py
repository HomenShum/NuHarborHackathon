import json
import pandas as pd
import re

filepath = r'hackathon-solution\Key.xlsx'
json_files = [
    r'hackathon-solution\All-MS\All-MS.json',
    r'hackathon-solution\All-CS\All-CS.json',
]
output_prefixes = [
    'hackathon-solution/All-MS/',
    'hackathon-solution/All-CS/',
]

# Read the Excel file
df = pd.read_excel(filepath)

def remove_irrelevant_items(data):
    irrelevant_keys = ['UUID', 'GPT Summary', 'AlertID', 'AlertTimestamp', 'Affected_Device', 'Affected_User', 'event_id', 'event_timestamp', 'event_time', 'endpoint_id', 'host', 'Hostname', 'IP', 'OS', 'User', 'destination_port', 'destination_ip']

    if isinstance(data, dict):
        for key in irrelevant_keys:
            if key in data:
                del data[key]
        
        for value in data.values():
            remove_irrelevant_items(value)

    elif isinstance(data, list):
        for item in data:
            remove_irrelevant_items(item)

    return data

def clean_value(value):
    # Remove any non-alphanumeric characters from the value
    return re.sub('[^0-9a-zA-Z]+', '', str(value))

def add_uuid(obj, df):
    raw_string = json.dumps(obj)

    for index, row in df.iterrows():
        max_uuid = None
        max_summary = None
        for column in ['Microsoft', 'CrowdStrike']:
            current_value = row[column]
            if current_value is not None and not pd.isnull(current_value):
                current_value_clean = clean_value(current_value)
                raw_string_clean = clean_value(raw_string)

                if current_value_clean.lower() in raw_string_clean.lower():
                    max_uuid = row['UUID']
                    max_summary = row['Summary']
                    break

        if max_uuid is not None:
            obj["UUID"] = max_uuid
            obj["Summary"] = max_summary
            break

def process_json_file(json_file, output_prefix):
    output_file = output_prefix + 'UUID_Summary.json'

    # Read the JSON file line by line and process each JSON object
    with open(json_file, 'r') as f:
        all_data = []
        for line in f:
            data = json.loads(line.strip())

            # Remove irrelevant keys
            data = remove_irrelevant_items(data)

            # Add UUID and Summary
            add_uuid(data, df)

            # Append the updated JSON object to the all_data list
            all_data.append(data)

    # Save the dataset to a new file
    with open(output_file, 'w') as f:
        for data in all_data:
            json.dump(data, f)
            f.write('\n')

# Process each JSON file
for json_file, output_prefix in zip(json_files, output_prefixes):
    process_json_file(json_file, output_prefix)
