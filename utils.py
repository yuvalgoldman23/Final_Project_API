import mysql.connector

#Returns true if the response is an error, false otherwise
def is_db_response_error(response):
    if isinstance(response, mysql.connector.Error):
        return True
    else:
        return False

def isNegative(num):
    if num < 0:
        return True
    else:
        return False

def filter_shortest_name_variants(streaming_services):
    main_providers = {}

    for service in streaming_services:
        provider_name = service["name"]
        new_first_word = provider_name.split()[0]

        # Check if the first word of the new provider name is part of existing provider names
        if not any(
            new_first_word in existing_provider.split()[0] or
            existing_provider.split()[0] in new_first_word
            for existing_provider in main_providers.keys()
        ):
            main_providers[provider_name] = service
        else:
            # Check if we need to replace the existing entry with a shorter name
            existing_provider = next(
                existing_provider for existing_provider in main_providers.keys()
                if new_first_word in existing_provider.split()[0] or existing_provider.split()[0] in new_first_word
            )
            # Compare lengths and replace if the current is shorter
            if len(provider_name) < len(existing_provider):
                del main_providers[existing_provider]  # Remove the longer one
                main_providers[provider_name] = service  # Add the shorter one

    return list(main_providers.values())