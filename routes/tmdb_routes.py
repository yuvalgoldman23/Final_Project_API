from flask import Blueprint, request, jsonify
import requests

tmdb_routes = Blueprint('tmdb_routes', __name__)


api_key = '2e07ce71cc9f7b5a418b824c87bcb76f'

@tmdb_routes.route('/api/Media_search', methods=['GET'])
def combine_search():
    query= request.args.get("query")
    movieurl=f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"
    tvurl=f"https://api.themoviedb.org/3/search/tv?api_key={api_key}&query={query}"
    response_movie=requests.get(movieurl)
    response_tv = requests.get(tvurl)
    if  response_movie.status_code == 200:
        movie_result= response_movie.json().get('results', [])
        t=5

    if  response_movie.status_code == 200:
        tv_result= response_tv.json().get('results', [])
    totalsearch=  movie_result+ tv_result
    return  jsonify(sorted(totalsearch,key= lambda  x: x["popularity"],reverse=True))


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

@tmdb_routes.route('/api/actor/<string:actor_id>', methods=['GET'])
def get_actor_info(actor_id):
    url = f"https://api.themoviedb.org/3/person/{actor_id}"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()
    return jsonify(data)


@tmdb_routes.route('/api/actor/movie_credits/<string:actor_id>', methods=['GET'])
def get_actor_movie_credits(actor_id):
    url = f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()
    return jsonify(data)

@tmdb_routes.route('/api/actor/tv_credits/<string:actor_id>', methods=['GET'])
def get_actor_tv_credits(actor_id):
    url = f"https://api.themoviedb.org/3/person/{actor_id}/tv_credits"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()
    return jsonify(data)




@tmdb_routes.route('/api/actor/combine_credits/<string:actor_id>', methods=['GET'])
def get_actor_combine_credits(actor_id):
    url = f"https://api.themoviedb.org/3/person/{actor_id}/tv_credits"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()
    url1 = f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits"
    params = {
        "api_key": api_key
    }

    response = requests.get(url1, params=params)
    data2 = response.json()
    t=5
    tv_credit_cast=[]

    tv_credit_cast =data.get('cast',[])
    movie_credit_cast = []

    movie_credit_cast = data2.get('cast', [])
    tv_credit_craw = []

    tv_credit_craw  = data.get('craw', [])
    movie_credit_craw = []

    movie_credit_craw = data2.get('crew', [])
    combined_cast_credits= movie_credit_cast+tv_credit_cast
    combined_craw_credits = movie_credit_craw + tv_credit_craw

    new_combined_cast_credits=[]
    for x in  combined_cast_credits:
        if "backdrop_path" in x:
            x.pop("backdrop_path")
        if "episode_count" in x:
            x.pop("episode_count")
        if "origin_country" in x:
            x.pop("origin_country")
        if "overview" in x:
            x.pop("overview")
        if "vote_average" in x:
            x.pop("vote_average")
        if "vote_average" in x:
            x.pop("vote_average")
        if "vote_average" in x:
            x.pop("vote_average")
        if "genre_ids" in x:
            x.pop("genre_ids")
        if "episode_count" in x:
            x.pop("episode_count")
        if "credit_id" in x:
            x.pop("credit_id")
        if "credit_id" in x:
            x.pop("credit_id")
        if "vote_count" in x:
            x.pop("vote_count")
        if "original_language" in x:
            x.pop("original_language")
        #new_combined_cast_credits.append(x)
    for x in  combined_craw_credits:
        if "backdrop_path" in x:
            x.pop("backdrop_path")
        if "episode_count" in x:
            x.pop("episode_count")
        if "origin_country" in x:
            x.pop("origin_country")
        if "overview" in x:
            x.pop("overview")
        if "vote_average" in x:
            x.pop("vote_average")
        if "vote_average" in x:
            x.pop("vote_average")
        if "vote_average" in x:
            x.pop("vote_average")
        if "genre_ids" in x:
            x.pop("genre_ids")
        if "episode_count" in x:
            x.pop("episode_count")
        if "credit_id" in x:
            x.pop("credit_id")
        if "credit_id" in x:
            x.pop("credit_id")
        if "vote_count" in x:
            x.pop("vote_count")
        if "original_language" in x:
            x.pop("original_language")
        #new_combined_cast_credits.append(x)



    ret={ "cast":sorted(combined_cast_credits,key= lambda  x: x["popularity"],reverse=True),
          "crew":sorted(combined_craw_credits,key= lambda  x: x["popularity"],reverse=True)
    }

    return jsonify(ret)


