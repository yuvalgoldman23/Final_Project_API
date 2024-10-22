# routes/watchlist_routes.py

from flask import Blueprint, request, jsonify, json
import aiohttp
import asyncio
import utils
from auth import auth_required
import services.watchlist_services as service
import routes.tmdb_routes as tmdb
import services.rating_services as rating_service
watchlists_routes = Blueprint('watchlists_routes', __name__)

# Get the watchlist's owner's ID
def get_watchlist_owner(watchlist_id):
    watchlist = service.get_watchlist_details_only(watchlist_id)
    return watchlist['User_ID']


# Receive a watchlist, which consists only of content IDs, and returns a website ready object including all needed details about its contents
# TODO  - finish after understanding the movies API
# TODO after finishing the Movies API, add a method to convert a watchlist's movie id's to a list of movie details?
def produce_client_ready_watchlist(watchlist_id, watchlist_items):
    if utils.is_db_response_error(watchlist_items):
        return "Database Error", 400
    watchlist_details = service.get_watchlist_details_only(watchlist_id)
    try:
        watchlist_name = watchlist_details['name']
    except TypeError:
        return 'Watchlist not found', 404
    #print("watchlist deets" , watchlist_details)
    finished_watchlist = []
    #print("watchlist items", watchlist_items)
    for watchlist_object in watchlist_items:
        #print("watchlist object", watchlist_object)
        # Add the watchlist item's ID to the client ready object in order to allow deletion of items from watchlist
        media_info = {'watchlist_item_id': watchlist_object['ID']}
        #print("watchlist object" , watchlist_object)
        is_movie = watchlist_object['is_movie']
        if is_movie:
            tmdb_info = (tmdb.get_movie_info(watchlist_object.get('TMDB_ID')))
        else:
            tmdb_info = tmdb.get_tv_show_info(watchlist_object.get('TMDB_ID'))
        if is_movie:
            tmdb_info = jsonify(tmdb_info)
        tmdb_info = tmdb_info.json
        media_info['title'] = tmdb_info['original_title'] if is_movie else tmdb_info['original_name']
        media_info['genres'] = [genre['name'] for genre in tmdb_info['genres']]
        media_info['tmdb_id'] = watchlist_object['TMDB_ID']
        media_info['is_movie'] = is_movie
        if tmdb_info.get('poster_path'):
            media_info['poster_path'] = "https://image.tmdb.org/t/p/original/" + tmdb_info['poster_path']
            media_info['small_poster_path'] = "https://image.tmdb.org/t/p/w200/" + tmdb_info['poster_path']
        else:
            media_info['poster_path'] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
            media_info['small_poster_path'] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"

        if tmdb_info['overview']:
            media_info['overview'] = tmdb_info['overview']
        else:
            media_info['overview'] = None
        if is_movie:
            media_info['release_date'] = tmdb_info.get('release_date')
        else:
            media_info['release_date'] = tmdb_info.get('first_air_date')

        if not media_info['release_date']:
            media_info['release_date'] = None
        if tmdb_info['vote_average']:
            media_info['tmdb_rating'] = tmdb_info['vote_average']
        else:
            media_info['tmdb_rating'] = None
        if tmdb_info.get('videos'):
            if not tmdb_info['videos']['results']:
                media_info['video_links'] = None
            else:
                media_info['video_links'] = [tmdb_info['videos']['results'][0]['key']]
            # TODO choose the right video to be here! e.g. trailer, youtube, official etc
            #print("provided the following video link",  media_info['video_links'])
        else:
            media_info['video_links'] = None
        user_id = watchlist_details['User_ID']
        user_rating, status_code = rating_service.get_rating_of_user(user_id, media_info['tmdb_id'],  watchlist_object['is_movie'])
        if status_code == 200:
            media_info['user_rating'] = user_rating['rating']
        else:
            media_info['user_rating'] = None
        # TODO add here the logos of the streaming services for this media in the USA? do that using my streaming function
        finished_watchlist.append(media_info)
    # If watchlist name wasn't set, give the watchlist a default name by its ID
    if not watchlist_name:
        watchlist_name = "Watchlist #"+ watchlist_details['ID']
    watchlist = {'Content': finished_watchlist, 'Name': watchlist_name, 'ID': watchlist_details['ID']}
    #print("finished watchlist" , finished_watchlist)
    return watchlist, 200


@watchlists_routes.route('/api/watchlists/test', methods=['GET'])
@auth_required
def get_main_watchlist(token_info):
    print("trying to get main watchlist")
    user_id = token_info.get('sub')
    db_response = service.get_main_watchlist(user_id)
    if utils.is_db_response_error(db_response):
        print("DB Error: " + str(db_response))
        return jsonify({'Error': str(db_response)}), 404
    else:
        #print("in get main watchlist route, db response is" + str(db_response))
        watchlist_id = db_response[0].get('ID')
        print("watchlist id is " + str(watchlist_id))
        watchlist_object = service.get_watchlist_by_id(watchlist_id)
        if utils.is_db_response_error(watchlist_object):
            json_response = jsonify({'Error': str(watchlist_object)})
            return json_response, 404
        #print("watchlist object is " + str(watchlist_object))
        client_ready_watchlist, status = produce_client_ready_watchlist(watchlist_id, watchlist_object)
        if status != 200:
            return jsonify({'Error': client_ready_watchlist}), status
        return jsonify(client_ready_watchlist), 200

'''Async get main watchlist'''
# TODO much faster, talk to Omer to understand how we can implement in the client
# TODO use the same strategy to fetch the ratings list
async def fetch_movie(session, content_id, is_movie, api_key, user_id, watchlist_id, item_id):
    movie_url = f"https://api.themoviedb.org/3/movie/{content_id}?api_key={api_key}&append_to_response=videos"
    tv_url = f"https://api.themoviedb.org/3/tv/{content_id}?api_key={api_key}&append_to_response=videos"

    async with session.get(movie_url if is_movie else tv_url) as response:
        if response.status == 200:
            data = await response.json()

            # Initialize media_info
            media_info = {}

            # Constructing the media_info object based on whether it's a movie or a series
            media_info['title'] = data.get('original_title') if is_movie else data.get('original_name')
            media_info['genres'] = [genre['name'] for genre in data.get('genres', [])]
            media_info['tmdb_id'] = content_id
            media_info['is_movie'] = is_movie

            # Poster paths
            poster_path = data.get('poster_path')
            if poster_path:
                media_info['poster_path'] = f"https://image.tmdb.org/t/p/original/{poster_path}"
                media_info['small_poster_path'] = f"https://image.tmdb.org/t/p/w200/{poster_path}"
            else:
                media_info['poster_path'] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
                media_info['small_poster_path'] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"

            # Overview
            media_info['overview'] = data.get('overview')

            # Release date
            media_info['release_date'] = data.get('release_date') if is_movie else data.get('first_air_date')

            # TMDB rating
            media_info['tmdb_rating'] = data.get('vote_average')

            # Video links
            videos = data.get('videos', {}).get('results', [])
            media_info['video_links'] = videos[0].get('key') if videos else None

            # User Rating
            user_rating, status_code = rating_service.get_rating_of_user(user_id, content_id, is_movie)
            if status_code == 200:
                media_info['user_rating'] = user_rating.get('rating')
            else:
                media_info['user_rating'] = None

            media_info['watchlist_item_id'] = item_id

            return media_info
        else:
            print(f"Had an error returning the info for {content_id} with response of {response.status}")
            return None  # Handle errors appropriately


async def fetch_movies(content_info, api_key, user_id, watchlist_id):
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(fetch_movie(session, item['TMDB_ID'], item['is_movie'], api_key, user_id, watchlist_id, item['ID']))
            for item in content_info
        ]
        return await asyncio.gather(*tasks)


def run_async(func, *args):
    return asyncio.run(func(*args))


def get_main_watchlist_data(user_id):
    """
    This helper function handles fetching the main watchlist and movie data.
    It returns the result as a Python dictionary, ready to be used internally or by the endpoint.
    """
    db_response = service.get_main_watchlist(user_id)

    if utils.is_db_response_error(db_response):
        return {'Error': str(db_response)}, 404

    watchlist_id = db_response[0].get('ID')

    watchlist_object = service.get_watchlist_by_id(watchlist_id)
    if utils.is_db_response_error(watchlist_object):
        return {'Error': str(watchlist_object)}, 404

    # Extract TMDB IDs and is_movie from the watchlist object
    extracted_watchlist = [
        {
            'TMDB_ID': item.get('TMDB_ID'),
            'is_movie': item.get('is_movie'),
            'ID': item.get('ID')
        }
        for item in watchlist_object
        if item.get('TMDB_ID') is not None
    ]

    api_key = '2e07ce71cc9f7b5a418b824c87bcb76f'

    # Fetch movies asynchronously, passing both TMDB_ID and is_movie
    movie_data_list = run_async(fetch_movies, extracted_watchlist, api_key, user_id, watchlist_id)

    # Filter out None values and construct the result
    result = [movie_data for movie_data in movie_data_list if movie_data is not None]

    # Return the result as a dictionary
    return {"Content": result, "ID": watchlist_id}, 200


@watchlists_routes.route('/api/watchlists', methods=['GET'])
@auth_required
def async_get_main_watchlist(token_info):
    """
    Endpoint for fetching the main watchlist. It uses the helper function
    and returns the result as a JSON response.
    """
    print("trying to get main watchlist")
    user_id = token_info.get('sub')

    # Call the helper function and get the result
    result, status_code = get_main_watchlist_data(user_id)

    # Return the result using jsonify for the API response
    return jsonify(result), status_code



@watchlists_routes.route('/api/watchlists', methods=['POST'])
@auth_required
def create_watchlist(token_info):
    data = request.json
    user_id = token_info.get('sub')
    watchlist_name = data.get('watchlist_name')
    db_response = service.create_watchlist(user_id, watchlist_name, False)
    if utils.is_db_response_error(db_response):
        return jsonify({"Error": str(db_response)}), 404
    else:
        new_watchlist_id = db_response
        return jsonify({'watchlist_id' : new_watchlist_id}), 201


@watchlists_routes.route('/api/watchlists/content', methods=['DELETE'])
@auth_required
def delete_content_from_watchlist(token_info):
    data = request.json
    if 'content_id' not in data:
        return jsonify({"error": "No content id provided in the request"}), 400
    watchlist_id = data['watchlist_id']
    content_id = data['content_id']
    user_id = token_info.get('sub')
    if not watchlist_id:
        watchlist_id = service.get_main_watchlist(user_id)[0].get('id')
    db_response = service.remove_watch_list_item(user_id, watchlist_id, content_id)
    if utils.is_db_response_error(db_response):
        return jsonify({'Error': str(db_response)}), 404
    else:
        return db_response

@watchlists_routes.route('/api/watchlists/<watchlist_id>', methods=['GET'])
def get_watchlist_by_id(watchlist_id):
    # TODO add user's watchlist ownership validation or not needed?
    # If wanting to protect by id, as toke_info and auth_required, and compare watchlist's owner id to the user id in token
    #user_id = token_info.get('sub')
    # Returns the watchlist items only
    db_response = service.get_watchlist_by_id(watchlist_id)
    if utils.is_db_response_error(db_response):
        print("error")
        return jsonify({'Error': str(db_response)}), 404
    else:
        client_watchlist, status = produce_client_ready_watchlist(watchlist_id, watchlist_items=db_response)
        if status != 200:
            return jsonify({"Error": client_watchlist}), status
        #print("client's watchlist is " , client_watchlist)
        return jsonify(client_watchlist), 200


from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import jsonify


@watchlists_routes.route('/api/watchlists/all', methods=['GET'])
@auth_required
def get_user_watchlists(token_info):
    #print("in get all")
    user_id = token_info.get('sub')
    db_response = service.get_user_watchlists(user_id)
    #print("db response " , db_response)
    # Check whether the DB has returned watchlists or an error
    if utils.is_db_response_error(db_response):
        return jsonify({'Error': str(db_response)}), 404
    else:
        all_watchlists = []
        #print("db response is " , db_response)
        for watchlist in db_response:
            if utils.is_db_response_error(db_response):
                continue
            watchlist_id = watchlist.get('ID')
            watchlist, status = (get_watchlist_by_id(watchlist_id))
            # Only add to watchlists list if no error has occurred during the DB transaction
            if status == 200:
                all_watchlists.append(watchlist.json)
        #print(all_watchlists)
        # Returns a list of json objects, each being a watchlist, including a content sub list and a Name attribute
        return jsonify({'watchlists' : all_watchlists}), 200


@watchlists_routes.route('/api/watchlists/content', methods=['POST'])
@auth_required
def add_movie_to_watchlist(token_info):
    data = request.json
    if 'content_id' not in data:
        return jsonify({"error": "No content id provided in the request"}), 400
    # TODO if the watchlist id is empty then add automatically to the user's main watchlist?
    watchlist_id = data.get('watchlist_id')
    content_id = data['content_id']
    user_id = token_info.get('sub')
    is_movie = data['is_movie']
    # Check if the user owns the watchlist they are about to add to
    if watchlist_id != '':
        if user_id != get_watchlist_owner(watchlist_id):
            return jsonify({"error": "You are not allowed to modify this watchlist"}), 403
    # TODO is the user_id necessary here? where is the validation that the watchlist belongs to the user adding the content?
    db_response, status = service.add_watch_list_item(user_id, content_id, watchlist_id, is_movie)
    if utils.is_db_response_error(db_response):
        return jsonify({'Error': str(db_response)}), 404
    else:
        if status == 200:
            return jsonify({'Success': f'Added {content_id} to watchlist', 'watchlist_object_id': db_response}), 200
        else:
            return jsonify({'Message': db_response}), 201

@watchlists_routes.route('/api/watchlists', methods=['DELETE'])
@auth_required
def delete_user_watchlist(token_info):
    data = request.json
    if 'watchlist_id' not in data:
        return jsonify({"error": "No content id provided in the request"}), 400
    user_id = token_info.get('sub')
    watchlist_id = data['watchlist_id']
    db_response = service.remove_watch_list(user_id, watchlist_id)
    # Check whether the DB has returned success or an error
    if utils.is_db_response_error(db_response):
        return jsonify({'Error': str(db_response)}), 404
    else:
        return db_response

@watchlists_routes.route('/api/watchlists/is_in_watchlist', methods=['GET', 'POST'])
@auth_required
def is_in_watchlist(token_info):
    user_id = token_info.get('sub')
    db_response = service.get_main_watchlist(user_id)
    if utils.is_db_response_error(db_response):
        print("DB Error: " + str(db_response))
        return jsonify({'Error': str(db_response)}), 404
    data = request.json
    if 'content_id' not in data or 'is_movie' not in data:
        return jsonify({"error": "No content id/is_movie provided in the request"}), 400
    else:
        #print("in get main watchlist route, db response is" + str(db_response))
        watchlist_id = db_response[0].get('ID')
        db_response, status = service.check_content_in_watchlist(watchlist_id, data['content_id'], data['is_movie'])
        if status != 200:
            return jsonify({"error": "DB error"}), status
        else:
            return jsonify({"is_in_watchlist": db_response}), 200

