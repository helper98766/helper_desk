import json

def reading_output_file(output_file):
    with open(output_file, "r") as file:
        data = json.load(file)
        for item in data:
            return item["victim"]["ip"]

def convert_json_to_dict(data):  # This is specific to pushing data into a database. Explore options to include in the module itself.
    with open(data, "r") as file:
        dict_data = json.load(file)
    return dict_data

# Combine above two folders
# File naming convention
# Move convert_json_to_dict function here