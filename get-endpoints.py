import comics
import json

# Fetch the list of endpoints
endpoints = comics.directory.listall()

# Define the file path
file_path = 'public/comics.json'

# Save the list to a JSON file
with open(file_path, 'w') as json_file:
    json.dump(endpoints, json_file, indent=4)

print(f"Endpoints saved to {file_path}")