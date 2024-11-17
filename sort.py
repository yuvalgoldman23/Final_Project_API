import json

# Load the JSON data from a file
with open('regions.json', 'r') as file:  # Replace 'input_file.json' with your actual file name
    data = json.load(file)

# Sort the list of regions by the 'name' key
data["regions"].sort(key=lambda region: region["name"])

# Write the sorted data back to a new JSON file
with open('regions.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Data has been sorted and written to regions.json")
