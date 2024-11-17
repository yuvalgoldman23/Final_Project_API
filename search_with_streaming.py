import aiohttp
import asyncio
from flask import Flask, jsonify, request
import time
from concurrent.futures import ThreadPoolExecutor

TMDB_API_KEY = '2e07ce71cc9f7b5a418b824c87bcb76f'  # Replace with your TMDB API key

app = Flask(__name__)

# Asynchronous function to fetch streaming services data
async def media_page_streaming_services(content_id, content_type):
    tmdb_url = f"https://api.themoviedb.org/3/{content_type}/{content_id}/watch/providers?api_key={TMDB_API_KEY}"
    headers = {
        "api_key": f"{TMDB_API_KEY}",
        "accept": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(tmdb_url, headers=headers) as response:
                data = await response.json()
                streaming_providers = data.get("results", {})
                for country, info in streaming_providers.items():
                    streaming_providers[country] = info.get('flatrate', [])  # Retain 'flatrate' if available
                return streaming_providers
        except Exception as error:
            print("TMDB Error", error)
            return {}

# Function to run for each result in parallel (async version)
async def process_result(result):
    content_id = result['id']
    content_type = 'movie' if result['media_kind'] == 'movie' else 'tv'

    # Fetch streaming data concurrently for each result
    streaming_services = await media_page_streaming_services(content_id, content_type)

    # Add the streaming providers data to the result
    result['streaming_services'] = streaming_services
    return result

# Function to perform the search (asynchronous)
@app.route('/api/Media_search', methods=['GET'])
async def combine_search():
    query = request.args.get("query")
    movieurl = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&include_adult=false"
    tvurl = f"https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}&query={query}&include_adult=false"

    # Request movie and TV search results
    async with aiohttp.ClientSession() as session:
        try:
            # Make concurrent requests for both movie and TV search results
            movie_response, tv_response = await asyncio.gather(
                session.get(movieurl),
                session.get(tvurl)
            )

            movie_result = []
            tv_result = []

            if movie_response.status == 200:
                movie_result = await movie_response.json()
                movie_result = movie_result.get('results', [])
                for m in movie_result:
                    m['media_kind'] = 'movie'

            if tv_response.status == 200:
                tv_result = await tv_response.json()
                tv_result = tv_result.get('results', [])
                for m in tv_result:
                    m['media_kind'] = 'tv'

            # Combine the movie and TV results
            totalsearch = movie_result + tv_result

            # Set default poster if missing
            for result in totalsearch:
                if not result.get("poster_path"):
                    result["poster_path"] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
                    result["small_poster_path"] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
                else:
                    result['poster_path'] = "https://image.tmdb.org/t/p/original" + result['poster_path']
                    result['small_poster_path'] = "https://image.tmdb.org/t/p/w200" + result['poster_path']

            # Use asyncio to process results in parallel
            # We can also optimize using a ThreadPoolExecutor for the async call batching if needed
            processed_results = await asyncio.gather(*[process_result(result) for result in totalsearch])

            # Return processed results sorted by popularity
            return jsonify(sorted(processed_results, key=lambda x: x["popularity"], reverse=True))

        except Exception as error:
            return jsonify({"error": "Error fetching data from TMDB", "message": str(error)}), 500


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)  # Set use_reloader=False to avoid re-running async code
