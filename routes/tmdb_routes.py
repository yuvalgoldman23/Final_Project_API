from flask import Blueprint, request, jsonify
import requests

tmdb_routes = Blueprint('tmdb_routes', __name__)


api_key = '2e07ce71cc9f7b5a418b824c87bcb76f'


@tmdb_routes.route('/api/movie/all', methods=['GET'])
def get_all_movies():
    all_movies = []
    page = 1

    while True:
        url = f"https://api.themoviedb.org/3/discover/movie"
        params = {
            "api_key": api_key,
            "page": page
        }

        response = request.get(url, params=params)
        data = response.json()

        if 'results' in data and len(data['results']) > 0:
            all_movies.extend(data['results'])
            page += 1
        else:
            break
        if page > 100:
            break
    return all_movies


@tmdb_routes.route('/api/tv/trending', methods=['GET'])
def get_trending_tv_shows():
    url = f"https://api.themoviedb.org/3/trending/tv/week?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        trending_tv_shows = response.json().get('results', [])
        return trending_tv_shows
    else:
        print("Failed to fetch trending TV shows:", response.status_code)
        return []


@tmdb_routes.route('/api/movie/trending', methods=['GET'])
def get_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        trending_tv_shows = response.json().get('results', [])
        return trending_tv_shows
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

    return data


@tmdb_routes.route('/api/tv/cast/<string:tv_show_id>', methods=['GET'])
def get_tv_cast(tv_show_id):
    url = f"https://api.themoviedb.org/3/tv/{tv_show_id}/credits"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data['cast']


@tmdb_routes.route('/api/movie/cast/<string:movie_id>', methods=['GET'])
def get_movie_cast(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data['cast']


@tmdb_routes.route('/api/movie/<string:movie_id>', methods=['GET'])
def get_movie_info(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data