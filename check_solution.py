import json

# Define list of JSON files
json_files = [
    r'C:\Users\hshum\OneDrive\Desktop\Python\hackathon\NuHarborHackathon-main\hackathon-solution\All-MS\UUID_Summary.json',
    r'C:\Users\hshum\OneDrive\Desktop\Python\hackathon\NuHarborHackathon-main\hackathon-solution\All-CS\UUID_Summary.json'
]

# Read JSON files and process each object
for json_file in json_files:
    print(f"Processing {json_file}...")

    # Read the JSON file line by line and process each JSON object
    with open(json_file, 'r') as f:
        total_dicts = 0
        total_uuids = 0
        for line in f:
            try:
                data = json.loads(line.strip())
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON object in {json_file}...")
                continue

            # Count total number of UUIDs and JSON dictionaries
            if isinstance(data, dict):
                total_dicts += 1
                if 'UUID' in data:
                    total_uuids += 1


    
    # Output total number of UUIDs and JSON dictionaries
    print(f"Total number of JSON dictionaries: {total_dicts}")
    print(f"Total number of UUIDs: {total_uuids}")
    if total_dicts == total_uuids:
        print("The total number of UUIDs is equal to the number of JSON dictionaries.\n")
    else:
        print("The total number of UUIDs is not equal to the number of JSON dictionaries.\n")
