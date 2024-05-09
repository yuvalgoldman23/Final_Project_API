import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
api_key = '2e07ce71cc9f7b5a418b824c87bcb76f'
def get_all_movies(api_key):
    all_movies = []
    page = 1

    while True:
        url = f"https://api.themoviedb.org/3/discover/movie"
        params = {
            "api_key": api_key,
            "page": page
        }

        response = requests.get(url, params=params)
        data = response.json()

        if 'results' in data and len(data['results']) > 0:
            all_movies.extend(data['results'])
            page += 1
        else:
            break
        if page >100:
            break
    return all_movies

def main():
    # Replace 'YOUR_API_KEY' with your actual API key
    movie_id = 1011985
    tv_show_id=32692

    movie_info = get_movie_info(api_key, movie_id)
    tv_info = get_tv_show_info(api_key, tv_show_id)
    cast_info= get_TV_cast(api_key,  tv_show_id)
    movie_cast=get_movie_cast(api_key, movie_id)
    print (  get_trending_movies(api_key))
    t=5

@app.route('/data/tv/trand', methods=['GET'])
def get_trending_tv_shows():
    url = f"https://api.themoviedb.org/3/trending/tv/week?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        trending_tv_shows = response.json().get('results', [])
        return trending_tv_shows
    else:
        print("Failed to fetch trending TV shows:", response.status_code)
        return []

@app.route('/data/movie/trand', methods=['GET'])
def get_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        trending_tv_shows = response.json().get('results', [])
        return trending_tv_shows
    else:
        print("Failed to fetch trending TV shows:", response.status_code)
        return []

@app.route('/data/tv/<string:tv_show_id>', methods=['GET'])
def get_tv_show_info( tv_show_id):
    url = f"https://api.themoviedb.org/3/tv/{tv_show_id}"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data

@app.route('/data/tv/cast/<string:tv_show_id>', methods=['GET'])
def get_TV_cast(  tv_show_id):
    url = f"https://api.themoviedb.org/3/tv/{ tv_show_id}/credits"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data['cast']


@app.route('/data/movie/cast/<string:movie_id>', methods=['GET'])
def get_movie_cast( movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data['cast']

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/data/movie/<string:movie_id>', methods=['GET'])
def get_movie_info(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data



if __name__ == "__main__":
   # main()
   app.run(debug=True)

