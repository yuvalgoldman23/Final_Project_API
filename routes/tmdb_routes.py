from flask import Blueprint, request, jsonify
import requests

tmdb_routes = Blueprint('tmdb_routes', __name__)


api_key = '2e07ce71cc9f7b5a418b824c87bcb76f'


@tmdb_routes.route('/api/tv/trending', methods=['GET'])
def get_trending_tv_shows():
    url = f"https://api.themoviedb.org/3/trending/tv/week?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        trending_tv_shows = response.json().get('results', [])
        return jsonify(trending_tv_shows)
    else:
        print("Failed to fetch trending TV shows:", response.status_code)
        return []


@tmdb_routes.route('/api/movie/trending', methods=['GET'])
def get_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        trending_tv_shows = response.json().get('results', [])
        return jsonify(trending_tv_shows)
    else:
        print("Failed to fetch trending TV shows:", response.status_code)
        return []


@tmdb_routes.route('/api/tv/<string:tv_show_id>', methods=['GET'])
def get_tv_show_info(tv_show_id):
    url = f"https://api.themoviedb.org/3/tv/{tv_show_id}"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()
    return jsonify(data)


@tmdb_routes.route('/api/tv/cast/<string:tv_show_id>', methods=['GET'])
def get_tv_cast(tv_show_id):
    url = f"https://api.themoviedb.org/3/tv/{tv_show_id}/credits"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()
    return jsonify(data['cast'])


@tmdb_routes.route('/api/movie/cast/<string:movie_id>', methods=['GET'])
def get_movie_cast(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()
    return jsonify(data['cast'])


@tmdb_routes.route('/api/movie/<string:movie_id>', methods=['GET'])
def get_movie_info(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()
    return jsonify(data)