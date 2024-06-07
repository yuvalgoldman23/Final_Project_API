# routes/watchlist_routes.py

from flask import Blueprint, request, jsonify
from auth import auth_required
from services.watchlist_services import get_user_watchlist, add_watch_list_item, remove_watch_list_item

watchlist_routes = Blueprint('watchlists_routes', __name__)


@watchlist_routes.route('/api/watchlist', methods=['GET'])
@auth_required
def get_watchlist(token_info):
    user_id = token_info.get('sub')
    return get_user_watchlist(user_id)



# Receive a watchlist, which consists only of content IDs, and returns a website ready object including all needed details about its contents
# TODO  - finish after understanding the movies API
def produce_watchlist(watchlist):
    finished_watchlist = watchlist
    return finished_watchlist
# TODO after finishing the Movies API, add a method to convert a watchlist's movie id's to a list of movie details?


@watchlist_routes.route('/api/watchlist/content', methods=['DELETE'])
@auth_required
def delete_content_from_watchlist(token_info):
    data = request.json
    if 'watchlist_item_id' not in data:
        return jsonify({"error": "No content id provided in the request"}), 400
    watchlist_item_id = data['watchlist_item_id']
    user_id = token_info.get('sub')
    return remove_watch_list_item(user_id, watchlist_item_id)


@watchlist_routes.route('/api/watchlists/content', methods=['PUT'])
@auth_required
def add_movie_to_watchlist(token_info):
    data = request.json()
    if 'content_id' not in data:
        return jsonify({"error": "No content id provided in the request"}), 400
    content_id = data['content_id']
    user_id = token_info.get('sub')
    return add_watch_list_item(user_id, media_tmdb_id=content_id, )