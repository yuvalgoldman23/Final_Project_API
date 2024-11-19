import time
import asyncio

import requests
from flask import Blueprint, request, jsonify, current_app
import utils
from auth import auth_required
from dotenv import load_dotenv
import os
import aiohttp
from services.watchlist_services import get_watchlist_by_id, get_main_watchlist
from concurrent.futures import ThreadPoolExecutor
from collections import OrderedDict

# Load environment variables from .env
load_dotenv()

streaming_providers_routes = Blueprint('streaming_providers_routes', __name__)

# Fetch TMDB API key from environment variables
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")


def get_netflix_prices():
    # Access the scraper instance from the app's context
    scraper = current_app.netflix_scraper
    # Call the get_latest_prices function
    data = scraper.get_latest_prices()
    return data

def get_usa_prices():
    # Access the scraper instance
    scraper = current_app.usa_scraper
    # Call the get_latest_prices function
    data = scraper.get_latest_prices()
    return data


@streaming_providers_routes.route('/api/netflix_prices', methods=['GET'])
def get_netflix_prices_route():
    return get_netflix_prices()


@streaming_providers_routes.route('/api/netflix_price_region', methods=['GET'])
def get_netflix_prices_by_region():
    data = request.json
    if not data.get("region"):
        return jsonify({"error": "No region provided"}), 400
    scraper = current_app.netflix_scraper
    region_code = data.get("region")
    data = scraper.get_latest_price_by_region(region_code)
    return jsonify(data)


@streaming_providers_routes.route('/api/usa_prices', methods=['GET'])
def get_usa_prices_route():
    scraper = current_app.usa_scraper
    data = scraper.get_latest_prices()
    return jsonify(data)


def media_page_streaming_services(content_id, content_type):
    tmdb_url = f"https://api.themoviedb.org/3/{content_type}/{content_id}/watch/providers?api_key={TMDB_API_KEY}"
    headers = {
        "api_key": f"{TMDB_API_KEY}",
        "accept": "application/json"
    }
    params = {"api_key": TMDB_API_KEY}

    try:
        data = requests.get(tmdb_url, headers=headers).json()
        streaming_providers = data.get("results", {})
        for country, info in streaming_providers.items():
            data['results'][country] = info.get('flatrate', [])  # Retain 'flatrate' if available, else empty list
        # TODO shall we filter variants here or not? if so, use the function in utils, but first make sure it fits the new countries structure
        return streaming_providers
    except Exception as error:
        print("TMDB Error", error)
        return []


def merge_provider_counts(main_providers, new_providers):
    for provider_name, data in new_providers.items():
        # Check if the provider name contains "epix" (case insensitive)
        if 'epix' in provider_name.lower():
            provider_name = "MGM Plus"  # Rename the provider to "MGM Plus"

        new_first_word = provider_name.split()[0]
        if not any(
                new_first_word in existing_provider.split()[0] or
                existing_provider.split()[0] in new_first_word
                for existing_provider in main_providers.keys()
        ):
            # New provider name, add to main providers
            main_providers[provider_name] = data
        else:
            # If the provider already exists in main_providers, update it
            if provider_name in main_providers:
                # Ensure uniqueness of TMDB IDs by creating a set of (tmdb_id, is_movie) tuples
                existing_tmdb_ids = set(
                    (tmdb_obj['tmdb_id'], tmdb_obj['is_movie']) for tmdb_obj in main_providers[provider_name]["tmdb_ids"]
                )
                new_tmdb_ids = set(
                    (tmdb_obj['tmdb_id'], tmdb_obj['is_movie']) for tmdb_obj in data["tmdb_ids"]
                )

                # Combine the existing and new TMDB IDs (union ensures uniqueness)
                combined_tmdb_ids = list(existing_tmdb_ids.union(new_tmdb_ids))

                # Update the tmdb_ids list with the unique combined entries
                main_providers[provider_name]["tmdb_ids"] = [
                    {"tmdb_id": tmdb_id, "is_movie": is_movie} for tmdb_id, is_movie in combined_tmdb_ids
                ]

                # Update the count to reflect the number of unique TMDB IDs
                main_providers[provider_name]["count"] = len(main_providers[provider_name]["tmdb_ids"])

                # Ensure we keep the logo_path if it exists
                if "logo_path" in data and data["logo_path"]:
                    main_providers[provider_name]["logo_path"] = data["logo_path"]

async def fetch_tmdb_data(tmdb_url, params, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(tmdb_url, params=params, headers=headers) as response:
            if response.status == 429:
                await asyncio.sleep(3)
                return await fetch_tmdb_data(tmdb_url, params, headers)  # Retry after rate limit
            return await response.json()

async def produce_streaming_providers_list_for_content(content_id, content_type):
    tmdb_url = f"https://api.themoviedb.org/3/{content_type}/{content_id}/watch/providers"
    headers = {
        "api_key": f"{TMDB_API_KEY}",
        "accept": "application/json"
    }
    params = {"api_key": TMDB_API_KEY}

    try:
        data = await fetch_tmdb_data(tmdb_url, params, headers)
        streaming_providers = data.get("results", {})
        providers_by_territory = {}

        for territory, territory_data in streaming_providers.items():
            territory_providers = territory_data.get('flatrate', [])
            if territory_providers:
                providers_by_territory[territory] = [
                    {
                        "name": provider.get("provider_name"),
                        "logo_path": provider.get("logo_path"),
                        "provider_id": provider.get("provider_id"),
                        "display_priority": provider.get("display_priority")
                    }
                    for provider in territory_providers
                ]
        return providers_by_territory
    except Exception as error:
        print("TMDB Error", error)
        return {}

async def get_streaming_recommendation_data(watchlist):
    """
    This helper function processes the watchlist and gathers streaming provider data for all territories.
    It returns the result as a dictionary with sorted providers and the best providers for each territory.
    """
    territory_results = {}

    async def process_watchlist_item(watchlist_object):
        is_movie = 'movie' if watchlist_object.get("is_movie") else 'tv'
        tmdb_id = watchlist_object["TMDB_ID"]
        territories_providers = await produce_streaming_providers_list_for_content(tmdb_id, is_movie)

        territory_provider_counts = {}

        for territory, providers in territories_providers.items():
            if territory not in territory_provider_counts:
                territory_provider_counts[territory] = {}

            for provider in providers:
                provider_name = provider["name"]
                tmdb_id_object = {"tmdb_id": tmdb_id, "is_movie": watchlist_object.get("is_movie")}

                if provider_name not in territory_provider_counts[territory]:
                    territory_provider_counts[territory][provider_name] = {
                        "count": 1,
                        "tmdb_ids": [tmdb_id_object],
                        "logo_path": provider["logo_path"],  # Store the logo path
                        "provider_id": provider["provider_id"]  # Store the provider ID
                    }
                else:
                    territory_provider_counts[territory][provider_name]["count"] += 1
                    territory_provider_counts[territory][provider_name]["tmdb_ids"].append(tmdb_id_object)

        return territory_provider_counts

    async def gather_provider_data():
        tasks = [process_watchlist_item(watchlist_object) for watchlist_object in watchlist]
        results = await asyncio.gather(*tasks)

        for result in results:
            for territory, providers in result.items():
                if territory not in territory_results:
                    territory_results[territory] = {}
                merge_provider_counts(territory_results[territory], providers)

    await gather_provider_data()

    final_results = {}
    for territory, providers in territory_results.items():
        sorted_providers = sorted(providers.items(), key=lambda item: item[1]["count"], reverse=True)
        sorted_providers = OrderedDict(sorted_providers)

        if len(sorted_providers) > 0:
            top_value = next(iter(sorted_providers.values()))["count"]
            best_providers = {
                provider: data
                for provider, data in sorted_providers.items()
                if data["count"] == top_value
            }

            final_results[territory] = {
                "providers": sorted_providers,
                "best_providers": best_providers,
            }

    return final_results, 200 if final_results else 404

@streaming_providers_routes.route('/api/watchlists/streaming_recommendation', methods=['GET', 'POST'])
@auth_required
def streaming_recommendation(token_info):
    """
    Endpoint for fetching streaming provider recommendations for all available territories.
    """
    data = request.json

    if "watchlist_id" not in data:
        user_id = token_info.get('sub')
        db_response = get_main_watchlist(user_id)
        if utils.is_db_response_error(db_response):
            return jsonify({'Error': str(db_response)}), 404
        watchlist_id = db_response[0].get('ID')
    else:
        watchlist_id = data['watchlist_id']
    watchlist = get_watchlist_by_id(watchlist_id)
    result, status_code = asyncio.run(get_streaming_recommendation_data(watchlist))
    return jsonify(result, get_netflix_prices(), get_usa_prices()), status_code