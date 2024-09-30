import time

from flask import Blueprint, request, jsonify

import utils
from auth import auth_required
from dotenv import load_dotenv
import os
import requests
from services.watchlist_services import get_watchlist_by_id, get_main_watchlist
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import OrderedDict

# Load environment variables from .env
load_dotenv()

streaming_providers_routes = Blueprint('streaming_providers_routes', __name__)

# Fetch TMDB API key from environment variables
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")

# Returns the list of regions for which we have watch providers info via TMDB
# TODO should be used to create a selection menu for the regions to base our recommendations on
# TODO maybe just make the client have the list in it, since it'll always be the same
@streaming_providers_routes.route('/api/streaming-providers/regions', methods=['GET'])
def get_generally_available_regions():
    tmdb_url = 'https://api.themoviedb.org/3/watch/providers/regions'
    headers = {
        "api_key": f"{TMDB_API_KEY}",
        "accept": "application/json"
    }
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(tmdb_url, params=params, headers=headers)
    #print(response)
    return jsonify(response.json())

@streaming_providers_routes.route('/api/streaming-providers', methods=['GET'])
def get_streaming_providers_by_content_id():
    data = request.get_json()
    content_id = data['content_id']
    territory = data.get('territory', None)
    is_movie = data.get('is_movie', None)
    if not content_id or is_movie is None:
        return jsonify({"error": "Content ID, Content Type are required."}), 400
    if type(is_movie) not in [bool, int]:
        return jsonify({"error": "is_movie must be bool or int"}), 400
    # Default territory would be the USA
    if territory is None:
        territory = 'US'
    response = produce_streaming_providers_list_for_content(content_id, territory, 'movie' if is_movie else 'tv')
    if isinstance(response, requests.exceptions.RequestException):
        return jsonify({"TMDB Error": str(response)}), 404
    else:
        return jsonify({"Providers":response}), 200


def produce_streaming_providers_list_for_content(content_id, territory, content_type):
    # Fetch streaming providers from TMDB
    tmdb_url = f"https://api.themoviedb.org/3/{content_type}/{content_id}/watch/providers"
    headers = {
        "api_key": f"{TMDB_API_KEY}",
        "accept": "application/json"
    }
    params = {"api_key": TMDB_API_KEY}
    try:
        # TODO could we create some DB entries to replace this since the rate is quite limited?
        # TODO currently i wouldn't display providers in the watchlist page because we might pass the quota?
        response = requests.get(tmdb_url, params=params)
        # TODO currently sleep if the TMDB api blocks us, find another solution
        while response.status_code == 429:
            time.sleep(3)
            response = requests.get(tmdb_url, params=params)
        #print(f"tmdb url for {content_id} is {tmdb_url}")
        response.raise_for_status()
        data = response.json()
        #print("data is ", data)
        #print(f"response data for {content_id}", type(data.get("results").get("CA")))
        # 'flatrate' means "available on streaming"
        try:
            streaming_providers = data.get("results", {}).get(territory, {}).get("flatrate", [])
        except KeyError:
            streaming_providers = []
        # TODO - think about what to return if streaming_providers== None due to no flatrate available
        provider_info = [
            {
                "name": provider.get("provider_name"),
                "logo_path": provider.get("logo_path"),
                "provider_id": provider.get("provider_id"),
                "display_priority": provider.get("display_priority")
            }
            for provider in streaming_providers
        ]
        # todo return logo for a provider or let a different API endpoint do that from our local DB?
        return provider_info
    except requests.exceptions.RequestException as error:
        print("TMDB Error", error)
        return []

@auth_required
@streaming_providers_routes.route('/api/watchlists/streaming_recommendation', methods=['GET'])
def streaming_recommendation(token_info):
    data = request.json
    # If no watchlist id provided in the data, we'll recommend based on the user's main watchlist
    if "watchlist_id" not in data:
        user_id = token_info.get('sub')
        db_response = get_main_watchlist(user_id)
        if utils.is_db_response_error(db_response):
            print("DB Error: " + str(db_response))
            return jsonify({'Error': str(db_response)}), 404
        else:
            # print("in get main watchlist route, db response is" + str(db_response))
            watchlist_id = db_response[0].get('ID')
    # If we were provided with a watchlist id, produce the results for it
    else:
        watchlist_id = data['watchlist_id']
    # By default, return results for streaming in the US
    territory = data.get('territory', 'US')
    # Get the watchlist's content
    watchlist = get_watchlist_by_id(watchlist_id)
    #  Process the watchlist item-by-item
    def process_watchlist_item(watchlist_object):
        is_movie = 'movie' if watchlist_object.get("is_movie") else 'tv'
        tmdb_id = watchlist_object["TMDB_ID"]

        # Get the list of providers for the given content
        current_providers = produce_streaming_providers_list_for_content(tmdb_id, territory, is_movie)
        provider_counts = {}

        # Count occurrences and store TMDB IDs
        for provider in current_providers:
            provider_name = provider["name"]
            tmdb_id_object = [{"tmdb_id": tmdb_id, "is_movie": watchlist_object.get("is_movie")}]
            if provider_name not in provider_counts:
                provider_counts[provider_name] = {"count": 1, "tmdb_ids": tmdb_id_object}
            else:
                provider_counts[provider_name]["count"] += 1
                provider_counts[provider_name]["tmdb_ids"].append(tmdb_id_object[0])

        return provider_counts

    def merge_provider_counts(main_providers, new_providers):
        for provider_name, data in new_providers.items():
            if provider_name not in main_providers:
                main_providers[provider_name] = data
            else:
                main_providers[provider_name]["count"] += data["count"]
                main_providers[provider_name]["tmdb_ids"].extend(data["tmdb_ids"])

    providers = {}

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_watchlist_item, watchlist_object) for watchlist_object in watchlist]
        for future in as_completed(futures):
            new_providers = future.result()
            merge_provider_counts(providers, new_providers)

    # Sort providers by count in descending order
    sorted_providers = sorted(providers.items(), key=lambda item: item[1]["count"], reverse=True)
    sorted_providers = OrderedDict(sorted_providers)

    #print("Providers sorted best to worst", sorted_providers)

    if len(sorted_providers) == 0:
        return jsonify({"Error": "No streaming providers found"}), 404

    top_value = next(iter(sorted_providers.values()))["count"]

    # Collect all providers with the top count value
    best_providers = {provider: data for provider, data in sorted_providers.items() if data["count"] == top_value}

    # Return as JSON with both count and tmdb_ids
    return jsonify({"providers": sorted_providers, "best_providers": best_providers}), 200

    # TODO return max. value in the providers list? limit the list to only well known providers such as hulu, netflix, amazon, hbo , etc?
# TODO remove 'similar' named streaming services - e.g. with and without ads?