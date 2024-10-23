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
        for m in movie_result:
            m['media_kind']='movie'
    if  response_movie.status_code == 200:
        tv_result= response_tv.json().get('results', [])
        for m in tv_result:
            m['media_kind'] = 'tv'
    totalsearch=  movie_result+ tv_result
    for result  in totalsearch:
        if not result["poster_path"]:
            result["poster_path"] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
            result["small_poster_path"] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
        else:
            result['poster_path'] = "https://image.tmdb.org/t/p/original" + result['poster_path']
            result['small_poster_path'] = "https://image.tmdb.org/t/p/w200" + result['poster_path']
    return  jsonify(sorted(totalsearch,key= lambda  x: x["popularity"],reverse=True))


@tmdb_routes.route('/api/tv/trending', methods=['GET'])
def get_trending_tv_shows():
    url = f"https://api.themoviedb.org/3/trending/tv/week?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        trending_tv_shows = response.json().get('results', [])
        for tvshow in trending_tv_shows:
            if not tvshow["poster_path"]:
                tvshow["poster_path"] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
                tvshow["small_poster_path"] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
            else:
                tvshow['poster_path'] = "https://image.tmdb.org/t/p/original" + tvshow['poster_path']
                tvshow['small_poster_path'] = "https://image.tmdb.org/t/p/w200" + tvshow['poster_path']
        return jsonify(trending_tv_shows)
    else:
        print("Failed to fetch trending TV shows:", response.status_code)
        return []


@tmdb_routes.route('/api/movie/trending', methods=['GET'])
def get_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        trending_movies = response.json().get('results', [])
        for movie in trending_movies:
            if not movie["poster_path"]:
                movie["poster_path"] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
                movie["small_poster_path"] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
            else:
                movie['poster_path'] = "https://image.tmdb.org/t/p/original" + movie['poster_path']
                movie['small_poster_path'] = "https://image.tmdb.org/t/p/w200" + movie['poster_path']
        return jsonify(trending_movies)
    else:
        print("Failed to fetch trending Movies:", response.status_code)
        return []


@tmdb_routes.route('/api/tv/<string:tv_show_id>', methods=['GET'])
def get_tv_show_info(tv_show_id):
    url = f"https://api.themoviedb.org/3/tv/{tv_show_id}?language=en&append_to_response=recommendations,videos,credits"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()
    if not data.get("poster_path"):
        data["poster_path"] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
        data["small_poster_path"] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
    else:
        data['poster_path'] = "https://image.tmdb.org/t/p/original" + data['poster_path']
        data['small_poster_path'] = "https://image.tmdb.org/t/p/w200" + data['poster_path']
    if data["videos"]:
        data["video_links"] = data["videos"]["results"]
        if not data["video_links"]:
            data["video_links"] = []
        else:
            data["video_links"] = [data["videos"]["results"][0]["key"]]
        '''
        # First, check if there exists an 'official' video of type 'Trailer' from 'site' = YouTube
        for link in data["video_links"]:
            # TODO Currently we return a single video only, the first trailer found. Change the conditions/break if require something else
            if link["type"] == "official" and link["site"] == "YouTube" and link["site"] == "Trailer":
                data["video_links"] = link["key"]
                break
        '''
    data["recommendations"] = data.get('recommendations').get('results', [])
    
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
    # TODO remove or leave the append to response here? use this to understand https://developer.themoviedb.org/reference/movie-similar
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?append_to_response=recommendations,videos,credits"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()
    if not data.get("poster_path"):
        data["poster_path"] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
        data["small_poster_path"] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
    else:
        data['poster_path'] = "https://image.tmdb.org/t/p/original" + data['poster_path']
        data['small_poster_path'] = "https://image.tmdb.org/t/p/w200" + data['poster_path']
    if "videos" in data and "results" in data["videos"] and len(data["videos"]["results"]) > 0:
            data["video_links"] = data["videos"]["results"]
            if not data["video_links"]:
                data["video_links"] = []
            else:
                data["video_links"] = [data["videos"]["results"][0]["key"]]
            '''
            # First, check if there exists an 'official' video of type 'Trailer' from 'site' = YouTube
            for link in data["video_links"]:
                # TODO Currently we return a single video only, the first trailer found. Change the conditions/break if require something else
                if link["type"] == "official" and link["site"] == "YouTube" and link["site"] == "Trailer":
                    data["video_links"] = link["key"]
                    break
            '''
    if "credits" in data and "crew" in data["credits"]:
        # Find the director and the screenwriter in the crew data and assign as "director" and "screenwriter"
        data["director"] = next((person for person in data["credits"]["crew"] if person["job"] == "Director"), None)
        data["screenwriter"] = next(
            (person for person in data["credits"]["crew"] if person["job"] == "Screenplay"),
            next((person for person in data["credits"]["crew"] if person["job"] == "Writer"), None)
        )

    data["recommendations"] = data.get('recommendations').get('results', [])

    return data

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
    for credit in data["cast"]:
        if not credit["poster_path"]:
            credit["poster_path"] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
            credit["small_poster_path"] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
        else:
            credit['poster_path'] = "https://image.tmdb.org/t/p/original" + credit['poster_path']
            credit['small_poster_path'] = "https://image.tmdb.org/t/p/w200" + credit['poster_path']
    return jsonify(data)

@tmdb_routes.route('/api/actor/tv_credits/<string:actor_id>', methods=['GET'])
def get_actor_tv_credits(actor_id):
    url = f"https://api.themoviedb.org/3/person/{actor_id}/tv_credits"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()
    for credit in data["cast"]:
        if not credit["poster_path"]:
            credit["poster_path"] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
            credit["small_poster_path"] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
        else:
            credit['poster_path'] = "https://image.tmdb.org/t/p/original" + credit['poster_path']
            credit['small_poster_path'] = "https://image.tmdb.org/t/p/w200" + credit['poster_path']
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
    for t in tv_credit_cast:
        t['media_kind'] = 'tv'
    movie_credit_cast = []

    movie_credit_cast = data2.get('cast', [])
    for t in  movie_credit_cast:
        t['media_kind'] = 'movie'
    tv_credit_craw = []

    tv_credit_craw  = data.get('craw', [])
    for t in tv_credit_craw :
        t['media_kind'] = 'tv'
    movie_credit_craw = []

    movie_credit_craw = data2.get('crew', [])
    for t in movie_credit_craw:
        t['media_kind'] = 'movie'

    combined_cast_credits= movie_credit_cast+tv_credit_cast
    combined_craw_credits = movie_credit_craw + tv_credit_craw

    for credit in combined_cast_credits:
        if not credit["poster_path"]:
            credit["poster_path"] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
            credit["small_poster_path"] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
        else:
            credit['poster_path'] = "https://image.tmdb.org/t/p/original" + credit['poster_path']
            credit['small_poster_path'] = "https://image.tmdb.org/t/p/w200" + credit['poster_path']
    for credit in combined_craw_credits:
        if not credit["poster_path"]:
            credit["poster_path"] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
            credit["small_poster_path"] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
        else:
            credit['poster_path'] = "https://image.tmdb.org/t/p/original" + credit['poster_path']
            credit['small_poster_path'] = "https://image.tmdb.org/t/p/w200" + credit['poster_path']

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


