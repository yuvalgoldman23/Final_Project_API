import json


def sort_services_by_name(input_file, output_file):
    # Load JSON data from the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        providers = json.load(file)

    sorted_providers = {}

    # Sort services for each country code by provider name
    for country_code, services in providers.items():
        sorted_services = dict(sorted(services.items(), key=lambda item: item[1]))
        sorted_providers[country_code] = sorted_services

    # Write sorted data to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(sorted_providers, file, indent=4, ensure_ascii=False)


# Specify input and output file names
input_file = 'regions_providers.json'
output_file = 'sorted_regions_providers.json'

# Run the sorting function
sort_services_by_name(input_file, output_file)

print(f"Sorted data has been written to {output_file}")
