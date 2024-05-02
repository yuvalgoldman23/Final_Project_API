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

# TODO add a function to return by  territory?
@streaming_providers_routes.route('/api/streaming-providers', methods=['GET'])
def get_streaming_providers():
    content_id = request.args.get('content_id')
    territory = request.args.get('territory', None)
    # Content type is 'tv' or 'movie'
    content_type = request.args.get('content_type')
    if not content_id:
        return jsonify({"error": "Content ID and territory are required"}), 400
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
        return jsonify({"providers": provider_info}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500