# routes/watchlist_routes.py

from flask import Blueprint, request, jsonify, json

import utils
from auth import auth_required
import services.watchlist_services as service
import routes.tmdb_routes as tmdb
watchlists_routes = Blueprint('watchlists_routes', __name__)

# Get the watchlist's owner's ID
def get_watchlist_owner(watchlist_id):
    watchlist = service.get_watchlist_details_only(watchlist_id)
    return watchlist['User_ID']


# Receive a watchlist, which consists only of content IDs, and returns a website ready object including all needed details about its contents
# TODO  - finish after understanding the movies API
# TODO after finishing the Movies API, add a method to convert a watchlist's movie id's to a list of movie details?
def produce_client_ready_watchlist(watchlist_id, watchlist_items):
    watchlist_details = service.get_watchlist_details_only(watchlist_id)
    watchlist_name = watchlist_details['name']
    print("watchlist deets" , watchlist_details)
    finished_watchlist = []
    print("watchlist items", watchlist_items)
    for watchlist_object in watchlist_items:
        # Add the watchlist item's ID to the client ready object in order to allow deletion of items from watchlist
        media_info = {'watchlist_item_id': watchlist_object['ID']}
        print("watchlist object" , watchlist_object)
        if watchlist_object['is_movie']:
            tmdb_info = (tmdb.get_movie_info(watchlist_object['TMDB_ID']))
        else:
            tmdb_info = tmdb.get_tv_show_info(watchlist_object.tmdb_id)
        tmdb_info = tmdb_info.json
        media_info['title'] = tmdb_info['original_title']
        media_info['genres'] = [genre['name'] for genre in tmdb_info['genres']]
        # TODO change poster size to be editable by client request?
        media_info['poster_path'] = "https://image.tmdb.org/t/p/w94_and_h141_bestv2/" + tmdb_info['poster_path']
        # TODO add here the logos of the streaming services for this media in the USA? do that using my streaming function
        finished_watchlist.append(media_info)
    # If watchlist name wasn't set, give the watchlist a default name by its ID
    if not watchlist_name:
        watchlist_name = "Watchlist #"+ watchlist_details['ID']
    watchlist = {'Content': finished_watchlist, 'Name': watchlist_name}
    print("finished watchlist" , finished_watchlist)
    return watchlist


@watchlists_routes.route('/api/watchlists', methods=['GET'])
@auth_required
def get_main_watchlist(token_info):
    user_id = token_info.get('sub')
    db_response = service.get_main_watchlist(user_id)
    # TODO add user's watchlist ownership validation or not needed?
    if utils.is_db_response_error(db_response):
        return jsonify({'Error': db_response}), 404
    else:
        watchlist_id = db_response[0].get('ID')
        watchlist_object = service.get_watchlist_by_id(watchlist_id)
        return produce_client_ready_watchlist(watchlist_id, watchlist_object)

@watchlists_routes.route('/api/watchlists', methods=['POST'])
@auth_required
def create_watchlist(token_info):
    data = request.json
    user_id = token_info.get('sub')
    watchlist_name = data.get('watchlist_name')
    db_response = service.create_watchlist(user_id, watchlist_name, False)
    if utils.is_db_response_error(db_response):
        return db_response, 404
    else:
        new_watchlist_id = db_response
        return jsonify({'watchlist_id' : new_watchlist_id}), 201


@watchlists_routes.route('/api/watchlists/content', methods=['DELETE'])
@auth_required
def delete_content_from_watchlist(token_info):
    data = request.json
    if 'watchlist_item_id' not in data:
        return jsonify({"error": "No content id provided in the request"}), 400
    watchlist_item_id = data['watchlist_item_id']
    user_id = token_info.get('sub')
    db_response = service.remove_watch_list_item(user_id, watchlist_item_id)
    if utils.is_db_response_error(db_response):
        return jsonify({'Error': db_response}), 404
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
        return jsonify({'Error': db_response}), 404
    else:
        client_watchlist = produce_client_ready_watchlist(watchlist_id, watchlist_items=db_response)
        print("client's watchlist is " , client_watchlist)
        return jsonify(client_watchlist), 200


@watchlists_routes.route('/api/users/watchlists/all', methods=['GET'])
@auth_required
def get_user_watchlists(token_info):
    user_id = token_info.get('sub')
    db_response = service.get_user_watchlists(user_id)
    # Check whether the DB has returned watchlists or an error
    if utils.is_db_response_error(db_response):
        return jsonify({'Error': db_response}), 404
    else:
        all_watchlists = []
        for watchlist in db_response:
            watchlist_id = watchlist.get('ID')
            watchlist, status = (get_watchlist_by_id(watchlist_id))
            all_watchlists.append(watchlist.json)
        print(all_watchlists)
        # Returns a list of json objects, each being a watchlist, including a content sub list and a Name attribute
        return jsonify({'watchlists' : all_watchlists}), 200
    # TODO here run the produce_client_ready_watchlist in a loop on all watchlists received here and return an object of watchlists, each being a return value from the produce function


@watchlists_routes.route('/api/watchlists/content', methods=['PUT'])
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
    db_response = service.add_watch_list_item(user_id, content_id, watchlist_id, is_movie)
    print("db response is " , db_response)
    if utils.is_db_response_error(db_response):
        return jsonify({'Error': db_response}), 404
    else:
        return db_response

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
        return jsonify({'Error': db_response}), 404
    else:
        return db_response
