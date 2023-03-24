import glob
import json
import pandas as pd
import re

json_files = glob.glob('hackathon-solution/All/*.json')
output_file = 'hackathon-solution/all_example_data.json'
filepath = r'hackathon-solution\Key.xlsx'

# Read the Excel file
df = pd.read_excel(filepath)

def clean_value(value):
    # Remove any non-alphanumeric characters from the value
    return re.sub('[^0-9a-zA-Z]+', '', str(value))

def find_matching_row(obj, df):
    raw_string = json.dumps(obj)
    
    for index, row in df.iterrows():
        for column in ['Microsoft', 'CrowdStrike']:
            current_value = row[column]
            if current_value is not None and not pd.isnull(current_value):
                current_value_clean = clean_value(current_value)
                raw_string_clean = clean_value(raw_string)

                if current_value_clean.lower() in raw_string_clean.lower():
                    return row
    return None

# Concatenate all JSON files together into a single file
all_data = []

for json_file in json_files:
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Find the matching row in the Excel file
    matching_row = find_matching_row(data, df)

    if matching_row is not None:
        # Append UUID and Summary to the JSON data
        data["UUID"] = matching_row["UUID"]
        data["Summary"] = matching_row["Summary"]

        # Add the updated JSON data to the list
        all_data.append(data)

# Save the concatenated JSON data to the output file
with open(output_file, 'w') as f:
    json.dump(all_data, f, indent=2)
