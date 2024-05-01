# routes/watchlists_routes.py

from flask import Blueprint, request, jsonify
from auth import auth_required

watchlists_routes = Blueprint('watchlists_routes', __name__)

@watchlists_routes.route('/api/watchlists', methods=['POST'])
@auth_required
def create_watchlist(token_info):
    data = request.json
    # Basic input validation
    token_user_id = token_info.get('sub')
    # TODO add a check for name length? probably more fitting to do in the client
    name = data.get('name', 'Untitled Watchlist')
    description = data.get('description', '')
    # Check if user exists
    user = users.get(token_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    # Generate watchlist ID
    watchlist_id = str(len(watchlists) + 1)
    # Create watchlist object
    new_watchlist = {
        "id": watchlist_id,
        "user_id": token_user_id,
        "name": name,
        "description": description,
        "movies": []
    }

    # Save watchlist to database
    watchlists[watchlist_id] = new_watchlist
    # TODO - decide how watchlists are saved
    #  currently we have a watchlists DB, and each user has a field with their watchlists ids
    # Update user's watchlist IDs
    user.setdefault('watchlists', []).append(watchlist_id)
    users[token_user_id] = user

    return jsonify(new_watchlist), 201


@watchlists_routes.route('/api/watchlists/<watchlist_id>', methods=['GET'])
@auth_required
def get_watchlist(token_info, watchlist_id):
    watchlist = watchlists.get(watchlist_id)
    # TODO - should watchlists be public? if so, no token or auth required....
    if watchlist:
        return jsonify(watchlist)
    else:
        return jsonify({"error": "Watchlist not found"}), 404


# TODO change/add to this so it only returns results for the currently logged in user??


@watchlists_routes.route('/api/users/<user_id>/watchlists', methods=['GET'])
@auth_required
def get_user_watchlists(token_info, user_id):
    data = request.json
    # Check that the user actually exists...
    user = users.get(user_id)
    token_user_id = token_info.get('sub')
    # Check that the user_id provided actually belongs to the logged in user
    if token_user_id != user_id:
        return jsonify({'error': 'User not authorized to perform this action'}), 400
    if user:
        user_watchlist_ids = user.get('watchlists', [])
        user_watchlists = [watchlists[watchlist_id] for watchlist_id in user_watchlist_ids]
        return jsonify(user_watchlists)
    else:
        return jsonify({"error": "User not found"}), 404


# TODO after finishing the Movies API, add a method to convert a watchlist's movie id's to a list of movie details?


@watchlists_routes.route('/api/watchlists/<watchlist_id>', methods=['DELETE'])
@auth_required
def delete_user_watchlist(token_info, watchlist_id):
    watchlist = watchlists.get(watchlist_id)
    user_id = watchlist['user_id']
    token_user_id = token_info.get('sub')
    if token_user_id != user_id:
        return jsonify({'error': "User not authorized to perform this action"}), 400
    if watchlist:
        # Remove watchlist from watchlists DB
        del watchlists[watchlist_id]
        # Remove watchlist from user's list
        user = users.get(user_id)
        if user and 'watchlists' in user:
            user['watchlists'].remove(watchlist_id)
            user[user_id] = user
            return jsonify({"message": f"Watchlist with ID {watchlist_id} has been deleted successfully."}), 200
        else:
            return jsonify({"error": f"Watchlist not found"}), 404


@watchlists_routes.route('/api/watchlists/<watchlist_id>', methods=['PUT'])
@auth_required
def update_watchlist(token_info, watchlist_id):
    watchlist = watchlists.get(watchlist_id)
    if watchlist:
        user_id = watchlist['user_id']
        token_user_id = token_info.get('sub')
        # Make sure that the watchlist belongs to the currently logged-in user
        if token_user_id != user_id:
            return jsonify({'error': f"the watchlist does not belong to the currently logged-in user"}), 400
        data = request.json
        if 'name' in data:
            # Update name
            if data['name'].isspace():
                watchlist['name'] = "Untitled Watchlist"
            else:
                watchlist['name'] = data['name']
        if 'description' in data:
            # Update description
            watchlist['description'] = data['description']
        if 'movie_id' in data:
            # Do not allow multiple additions of same movie
            if 'movie_id' not in watchlist['movies']:
                watchlist['movies'].append(data['movie_id'])
            else:
                watchlists[watchlist_id] = watchlist
                return jsonify({"error": f"Movie already in watchlist!"}), 400
        # Save updated watchlist to database
        watchlists[watchlist_id] = watchlist
    else:
        return jsonify({"error": f"Watchlist not found"}), 400


@watchlists_routes.route('/api/watchlists/<watchlist_id>/movies/<movie_id>', methods=['DELETE'])
@auth_required
def delete_movie_from_watchlist(token_info, watchlist_id, movie_id):
    watchlist = watchlists.get(watchlist_id)
    if not watchlist:
        return jsonify({"error": "Watchlist not found"}), 404
    # Check if movie exists in the watchlist
    user_id = watchlist['user_id']
    token_user_id = token_info.get('sub')
    # Make sure that the watchlist belongs to the currently logged-in user
    if token_user_id != user_id:
        return jsonify({'error': f"the watchlist does not belong to the currently logged-in user"}), 400
    for movie in watchlist['movies']:
        if movie['id'] == movie_id:
            # Delete the movie from the watchlist
            watchlist['movies'].remove(movie)
            # Save updated watchlist to database
            watchlists[watchlist_id] = watchlist
            return jsonify({"message": f"Movie with ID {movie_id} has been deleted from the watchlist"}), 200

    return jsonify({"error": f"Movie with ID {movie_id} not found in the watchlist"}), 404