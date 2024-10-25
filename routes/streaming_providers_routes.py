import time
import asyncio

import requests
from flask import Blueprint, request, jsonify
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


async def fetch_tmdb_data(tmdb_url, params, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(tmdb_url, params=params, headers=headers) as response:
            if response.status == 429:
                await asyncio.sleep(3)
                return await fetch_tmdb_data(tmdb_url, params, headers)  # Retry after rate limit
            return await response.json()


# TODO add territory to this, and separate the endpoint logic from the function itself so we could use it separately
async def produce_streaming_providers_list_for_content(content_id, territory, content_type):
    tmdb_url = f"https://api.themoviedb.org/3/{content_type}/{content_id}/watch/providers"
    headers = {
        "api_key": f"{TMDB_API_KEY}",
        "accept": "application/json"
    }
    params = {"api_key": TMDB_API_KEY}

    try:
        data = await fetch_tmdb_data(tmdb_url, params, headers)
        streaming_providers = data.get("results", {}).get(territory, {}).get("flatrate", [])
        provider_info = [
            {
                "name": provider.get("provider_name"),
                "logo_path": provider.get("logo_path"),
                "provider_id": provider.get("provider_id"),
                "display_priority": provider.get("display_priority")
            }
            for provider in streaming_providers
        ]
        return provider_info
    except Exception as error:
        print("TMDB Error", error)
        return []


def merge_provider_counts(main_providers, new_providers):
    for provider_name, data in new_providers.items():
        new_first_word = provider_name.split()[0]
        if not any(
                new_first_word in existing_provider.split()[0] or
                existing_provider.split()[0] in new_first_word
                for existing_provider in main_providers.keys()
        ):
            main_providers[provider_name] = data
        else:
            if provider_name in main_providers:
                main_providers[provider_name]["count"] += data["count"]
                main_providers[provider_name]["tmdb_ids"].extend(data["tmdb_ids"])


async def get_streaming_recommendation_data(watchlist_id, territory='US'):
    """
    This helper function processes the watchlist and gathers streaming provider data.
    It returns the result as a dictionary with sorted providers and the best providers.
    """
    watchlist = get_watchlist_by_id(watchlist_id)

    providers = {}

    async def process_watchlist_item(watchlist_object):
        is_movie = 'movie' if watchlist_object.get("is_movie") else 'tv'
        tmdb_id = watchlist_object["TMDB_ID"]
        current_providers = await produce_streaming_providers_list_for_content(tmdb_id, territory, is_movie)
        provider_counts = {}
        for provider in current_providers:
            provider_name = provider["name"]
            tmdb_id_object = [{"tmdb_id": tmdb_id, "is_movie": watchlist_object.get("is_movie")}]
            if provider_name not in provider_counts:
                provider_counts[provider_name] = {"count": 1, "tmdb_ids": tmdb_id_object}
            else:
                provider_counts[provider_name]["count"] += 1
                provider_counts[provider_name]["tmdb_ids"].append(tmdb_id_object[0])
        return provider_counts

    async def gather_provider_data():
        tasks = [process_watchlist_item(watchlist_object) for watchlist_object in watchlist]
        results = await asyncio.gather(*tasks)
        for new_providers in results:
            merge_provider_counts(providers, new_providers)

    await gather_provider_data()

    sorted_providers = sorted(providers.items(), key=lambda item: item[1]["count"], reverse=True)
    sorted_providers = OrderedDict(sorted_providers)

    if len(sorted_providers) == 0:
        print("No providers found for watchlist")
        return jsonify({"providers": {}, "best_providers": {}}), 404

    top_value = next(iter(sorted_providers.values()))["count"]
    best_providers = {provider: data for provider, data in sorted_providers.items() if data["count"] == top_value}
    return {"providers": sorted_providers, "best_providers": best_providers}, 200


@streaming_providers_routes.route('/api/watchlists/streaming_recommendation', methods=['GET', 'POST'])
@auth_required
def streaming_recommendation(token_info):
    """
    Endpoint for fetching streaming provider recommendations. It uses the helper function
    and returns the result as a JSON response.
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

    territory = data.get('territory', 'US')

    # Call the helper function and get the result asynchronously
    result, status_code = asyncio.run(get_streaming_recommendation_data(watchlist_id, territory))

    # Return the result using jsonify for the API response
    if status_code != 200:
        return jsonify({"providers": {}, "best_providers": {}}), status_code
    return jsonify(result), status_code
