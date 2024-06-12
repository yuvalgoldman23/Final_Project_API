from flask import Blueprint, request, jsonify
from auth import auth_required
from dotenv import load_dotenv
import os
import requests
from services.watchlist_services import get_watchlist_by_id
from collections import OrderedDict

# Load environment variables from .env
load_dotenv()

streaming_providers_routes = Blueprint('streaming_providers_routes', __name__)

# Fetch TMDB API key from environment variables
TMDB_API_KEY = os.getenv("TMDB_API_KEY")


# TODO add a function to return by  territory?
@streaming_providers_routes.route('/api/streaming-providers', methods=['GET'])
def get_streaming_providers_for_client():
    content_id = request.args.get('content_id')
    territory = request.args.get('territory', None)
    # Content type is 'tv' or 'movie'
    content_type = request.args.get('content_type')
    if not content_id or not content_type or not territory:
        return jsonify({"error": "Content ID, Content Type and territory are required"}), 400
    response = get_streaming_providers(content_id, territory, content_type)
    if isinstance(response, requests.exceptions.RequestException):
        return jsonify({"Error": response}), 404
    else:
        return jsonify({"Providers":response}), 200


def get_streaming_providers(content_id, territory, content_type):
    # Fetch streaming providers from TMDB
    tmdb_url = f"https://api.themoviedb.org/3/{content_type}/{content_id}/watch/providers"
    headers = {
        "api_key": f"{TMDB_API_KEY}",
        "accept": "application/json"
    }
    params = {"api_key": TMDB_API_KEY}
    try:
        response = requests.get(tmdb_url, params=params)
        response.raise_for_status()
        data = response.json()
        # 'flatrate' means "available on streaming"
        streaming_providers = data.get("results", {}).get(territory, {}).get("flatrate", [])
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
        return error

@streaming_providers_routes.route('/api/watchlists/streaming_recommendation', methods=['GET'])
def streaming_recommendation():
    data = request.json
    if "watchlist_id" not in data:
        return jsonify({"Error": "watchlist_id is required to proceed"}), 404
    watchlist_id = data['watchlist_id']
    territory = data['territory', 'US']
    watchlist = get_watchlist_by_id(watchlist_id)
    providers = {}
    for watchlist_object in watchlist:
        # TODO determine how to get the territory here?
        current_providers = get_streaming_providers(watchlist_object["content_id"], territory,  watchlist_object["content_type"])
        for provider in current_providers:
            # Count instances of every streaming provider offering content from our list
            providers[provider['name']] += 1
    sorted_providers = sorted(providers.items(), key=lambda item: item[1], reverse=True)
    sorted_providers = OrderedDict(sorted_providers)
    print(sorted_providers)
    # TODO return max. value in the providers list? limit the list to only well known providers such as hulu, netflix, amazon, hbo , etc?