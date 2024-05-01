from flask import Blueprint, request, jsonify
from auth import auth_required
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env
load_dotenv()


streaming_providers_routes = Blueprint('streaming_providers_routes', __name__)

# Fetch TMDB API key from environment variables
TMDB_API_KEY = os.getenv("TMDB_API_KEY")


# TODO remove territory from this request?
@streaming_providers_routes.route('/api/streaming-providers', methods=['GET'])
def get_streaming_providers():
    content_id = request.args.get('content_id')
    territory = request.args.get('territory')
    # Content type is 'tv' or 'movie'
    content_type = request.args.get('content_type')
    if not content_id or not territory:
        return jsonify({"error": "Content ID and territory are required"}), 400

    # Fetch streaming providers from TMDB
    tmdb_url = f"https://api.themoviedb.org/3/{content_type}/{content_id}/watch/providers"
    headers = {
        "Authorization": f"Bearer {TMDB_API_KEY}",
        "accept": "application/json"
    }
    params = {
        "territory": territory
    }

    try:
        response = requests.get(tmdb_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        streaming_providers = data.get("results", {}).get(territory, {}).get("flatrate", [])
        provider_names = [provider.get("provider_name") for provider in streaming_providers]
        return jsonify({"streaming_providers": provider_names}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500