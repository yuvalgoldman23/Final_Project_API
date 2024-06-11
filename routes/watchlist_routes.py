# routes/watchlist_routes.py

from flask import Blueprint, request, jsonify

import utils
from auth import auth_required
import services.watchlist_services as service

watchlists_routes = Blueprint('watchlists_routes', __name__)


# Receive a watchlist, which consists only of content IDs, and returns a website ready object including all needed details about its contents
# TODO  - finish after understanding the movies API
# TODO after finishing the Movies API, add a method to convert a watchlist's movie id's to a list of movie details?
def produce_client_ready_watchlist(watchlist):
    finished_watchlist = watchlist
    return finished_watchlist


@watchlists_routes.route('/api/watchlists', methods=['GET'])
@auth_required
def get_main_watchlist(token_info):
    user_id = token_info.get('sub')
    db_response = service.get_watchlist
    # TODO add user's watchlist ownership validation or not needed?
    if utils.is_db_response_error(db_response):
        return jsonify({'Error': db_response}), 404
    else:
        return db_response

@watchlists_routes.route('/api/watchlists', methods=['POST'])
@auth_required
def create_watchlist(token_info):
    data = request.json
    user_id = token_info.get('sub')
    watchlist_name = data['watchlist_name', '']
    db_response = service.create_watchlist(user_id, watchlist_name, is_main=False)
    if utils.is_db_response_error(db_response):
        return jsonify({"Error": db_response}), 404
    else:
        # TODO currently the service doesn't return the new ID - make sure to get fixed
        new_watchlist_id = db_response
        return new_watchlist_id


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
@auth_required
def get_watchlist_by_id(token_info, watchlist_id):
    # TODO add user's watchlist ownership validation or not needed?
    user_id = token_info.get('sub')
    db_response = service.get_watchlist_by_id(watchlist_id)
    if utils.is_db_response_error(db_response):
        return jsonify({'Error': db_response}), 404
    else:
        return db_response


@watchlists_routes.route('/api/users/watchlists/all', methods=['GET'])
@auth_required
def get_user_watchlists(token_info):
    user_id = token_info.get('sub')
    db_response = service.get_user_watchlists(user_id)
    # Check whether the DB has returned watchlists or an error
    if utils.is_db_response_error(db_response):
        return jsonify({'Error': db_response}), 404
    else:
        return db_response


@watchlists_routes.route('/api/watchlists/content', methods=['PUT'])
@auth_required
def add_movie_to_watchlist(token_info):
    data = request.json()
    if 'content_id' not in data:
        return jsonify({"error": "No content id provided in the request"}), 400
    content_id = data['content_id']
    user_id = token_info.get('sub')
    is_movie = data['is_movie', '']
    comment = data['comment', '']
    is_watched = data['is_watched', '']
    rating = data['rating', '']
    progress = data['progress', '']
    # TODO maybe some of these parameters aren't needed? currently left blank if not sent from client
    db_response = service.add_watch_list_item(user_id, content_id, is_movie, comment, is_watched, rating, progress)
    if utils.is_db_response_error(db_response):
        return jsonify({'Error': db_response}), 404
    else:
        return db_response

# TODO is this needed???
@watchlists_routes.route('/api/watchlists/<watchlist_id>', methods=['DELETE'])
@auth_required
def delete_user_watchlist(token_info, watchlist_id):
    user_id = token_info.get('sub')
    db_response = service.remove_watch_list(user_id, watchlist_id)
    # Check whether the DB has returned success or an error
    if utils.is_db_response_error(db_response):
        return jsonify({'Error': db_response}), 404
    else:
        return db_response
