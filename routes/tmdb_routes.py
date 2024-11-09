from flask import Blueprint, request, jsonify
import requests

from routes.streaming_providers_routes import media_page_streaming_services

tmdb_routes = Blueprint('tmdb_routes', __name__)


api_key = '2e07ce71cc9f7b5a418b824c87bcb76f'

@tmdb_routes.route('/api/Media_search', methods=['GET'])
def combine_search():
    query= request.args.get("query")
    movieurl=f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}&include_adult=false"
    tvurl=f"https://api.themoviedb.org/3/search/tv?api_key={api_key}&query={query}&include_adult=false"
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
    if data.get("videos") and data.get("videos").get("results"):
        data["video_links"] = data["videos"]["results"]
        if not data.get("video_links"):
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

    data['streaming_services'] = media_page_streaming_services(tv_show_id, "tv")
    
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

    data['streaming_services'] = media_page_streaming_services(movie_id, "movie")

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
    url_tv = f"https://api.themoviedb.org/3/person/{actor_id}/tv_credits"
    url_movie = f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits"
    params = {"api_key": api_key}

    # Fetch TV and movie credits
    response_tv = requests.get(url_tv, params=params)
    response_movie = requests.get(url_movie, params=params)
    data_tv = response_tv.json()
    data_movie = response_movie.json()

    # Separate cast and crew credits for both TV and movie
    tv_credit_cast = data_tv.get('cast', [])
    movie_credit_cast = data_movie.get('cast', [])
    tv_credit_crew = data_tv.get('crew', [])
    movie_credit_crew = data_movie.get('crew', [])

    # Assign media type
    for credit in tv_credit_cast + tv_credit_crew:
        credit['media_kind'] = 'tv'
    for credit in movie_credit_cast + movie_credit_crew:
        credit['media_kind'] = 'movie'

    # Combine cast credits
    combined_cast_credits = tv_credit_cast + movie_credit_cast

    # Combine crew credits and consolidate roles
    combined_crew_credits = {}
    for credit in tv_credit_crew + movie_credit_crew:
        key = (credit['id'], credit['media_kind'], credit['title'])
        if key not in combined_crew_credits:
            combined_crew_credits[key] = credit
        else:
            combined_crew_credits[key]['job'] += f", {credit['job']}"

    # Convert crew dictionary back to a list
    consolidated_crew_credits = list(combined_crew_credits.values())

    # Set default or construct poster paths
    for credit in combined_cast_credits + consolidated_crew_credits:
        if not credit.get("poster_path"):
            credit["poster_path"] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
            credit["small_poster_path"] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
        else:
            credit['poster_path'] = "https://image.tmdb.org/t/p/original" + credit['poster_path']
            credit['small_poster_path'] = "https://image.tmdb.org/t/p/w200" + credit['poster_path']

    # Return sorted cast and crew credits
    ret = {
        "cast": sorted(combined_cast_credits, key=lambda x: x["popularity"], reverse=True),
        "crew": sorted(consolidated_crew_credits, key=lambda x: x["popularity"], reverse=True)
    }
    return jsonify(ret)



