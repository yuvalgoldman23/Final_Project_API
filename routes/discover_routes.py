from flask import Blueprint, request, jsonify
import requests

discover_routes = Blueprint('discover_routes', __name__)

api_key = '2e07ce71cc9f7b5a418b824c87bcb76f'


API_KEY = "YOUR_API_KEY"
BASE_URL = "https://api.themoviedb.org/3"
AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmM2NhNmMxMWVhZjQzNDY1YTE4MTRmYTNhMjQ0MGYzNyIsIm5iZiI6MTcyODczODUxMS4yNDc2OTYsInN1YiI6IjY1YmZiZTE3MDMxZGViMDE4M2YxNjhjYiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.hZkDyMAhf2L4PtJ5W8T4bC0M5kojxLj9XEK9oN5qkl0"

headers = {
    "accept": "application/json",
    "Authorization": AUTH_TOKEN
}


def construct_query(data, is_movie):
    # Default query parameters
    query_parts = [
        "language=en-US",
        "sort_by=popularity.desc"
        # TODO maybe remove this part? Since the client's list allows non flatrate providers too
        "with_watch_monetization_types=flatrate"
    ]

    # Optional parameters
    if is_movie:
        # TODO check if gte works with only a year provided!
        if min_year := data.get("year"):
            query_parts.append(f"primary_release_date.gte={min_year}-01-01")
    else:
        # TODO check if gte even works here
        if min_year := data.get("year"):
            query_parts.append(f"first_air_date.gte={min_year}-01-01")
    if min_vote_average := data.get("vote_average"):
        query_parts.append(f"vote_average.gte={min_vote_average}")
    if country_code := data.get("country_code"):
        if region := data.get("region"):
            query_parts.append(f"with_origin_country={country_code}")
            query_parts.append(f"watch_region={region}")
    if provider_id := data.get("provider"):
        query_parts.append(f"with_watch_providers={provider_id}")
    if genres := data.get("genres"):
        genre_string = ",".join(genres) if isinstance(genres, list) else genres
        query_parts.append(f"with_genres={genre_string}")

    # Combine query parts into a single string
    query = "&".join(query_parts)
    return query


@discover_routes.route('/api/discover', methods=['POST', 'GET'])
def discover():
    movie_url=f"https://api.themoviedb.org/3/discover/movie?include_adult=false&"
    tv_url=f"https://api.themoviedb.org/3/discover/tv?include_adult=false&"
    # TODO think on how we could combine the tv and movies results in the case of a mixed request
    data = request.get_json()
    content_type = data.get("content_type")
    if content_type == "movie":
        query_movie = construct_query(data, is_movie=True)
        tmdb_response = requests.get(movie_url + query_movie, headers=headers)
        print("tmdb response: ", tmdb_response.json())
        return tmdb_response.json().get("results") if tmdb_response.status_code == 200 else tmdb_response.text
    elif content_type == "tv":
        query_tv = construct_query(data, is_movie=False)
        tmdb_response = requests.get(tv_url + query_tv, headers=headers)
        return tmdb_response.json().get("results") if tmdb_response.status_code == 200 else tmdb_response.text
    # "Mixed" case
    else:
        query_movie = construct_query(data, is_movie=False)
        tmdb_response_movie = requests.get(movie_url + query_movie, headers=headers)
        query_tv = construct_query(data, is_movie=True)
        tmdb_response_tv = requests.get(tv_url + query_tv, headers=headers)
        if tmdb_response_movie.status_code == 200 and tmdb_response_tv.status_code == 200:
            tmdb_response = tmdb_response_movie.json().get("results") + tmdb_response_tv.json().get("results")
            # Sort the mixed response by the content popularity
            return jsonify(sorted(tmdb_response, key=lambda x: x["popularity"], reverse=True))


