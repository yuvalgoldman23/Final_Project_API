# routes/lists_routes.py

from flask import Blueprint, request, jsonify
from auth import auth_required
import routes.tmdb_routes as tmdb
import services.rating_services as rating_service
lists_routes = Blueprint('lists_routes', __name__)

# TODO currently, this consists of the old watchlists routes, where  we let a user create multiple watchlists

@lists_routes.route('/api/watchlists', methods=['POST'])
@auth_required
def create_watchlist(token_info):
    data = request.json
    print("here")
    # Basic input validation
    token_user_id = token_info.get('sub')
    # TODO add a check for name length? probably more fitting to do in the client
    name = data.get('name', 'Untitled Watchlist')
    print("here")
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
    watchlists.append(new_watchlist)
    # TODO - decide how watchlists are saved
    #  currently we have a watchlists DB, and each user has a field with their watchlists ids
    # Update user's watchlist IDs
    user.setdefault('watchlists', []).append(watchlist_id)
    users[token_user_id] = user
    print(users)
    return jsonify(new_watchlist), 201


@lists_routes.route('/api/watchlists/<watchlist_id>', methods=['GET'])
@auth_required
def get_watchlist(token_info, watchlist_id):
    # PLACEHOLDER until DB implementation and queries
    my_watchlist = None
    for watchlist in watchlists:
        if watchlist['id'] == watchlist_id:
            my_watchlist = produce_watchlist(watchlist)
            break
    # TODO - should watchlists be public? if so, no token or auth required....
    if my_watchlist:
        return jsonify(my_watchlist)
    else:
        return jsonify({"error": "Watchlist not found"}), 404



# Receive a watchlist, which consists only of content IDs, and returns a website ready object including all needed details about its contents
# TODO  - finish after understanding the movies API
def produce_watchlist(watchlist):
    finished_watchlist = watchlist
    return finished_watchlist


# TODO change/add to this so it only returns results for the currently logged in user??


@lists_routes.route('/api/users/watchlists', methods=['GET'])
@auth_required
def get_user_watchlists(token_info):
    # Check that the user actually exists...
    user_id = token_info.get('sub')
    user = users.get(user_id)
    if user:
        user_watchlist_ids = user.get('watchlists', [])
        user_watchlists = [watchlist for watchlist in watchlists if watchlist.get('id') in user_watchlist_ids]
        return jsonify(user_watchlists)
    else:
        return jsonify({"error": "User not found"}), 404


# TODO after finishing the Movies API, add a method to convert a watchlist's movie id's to a list of movie details?


@lists_routes.route('/api/watchlists/<watchlist_id>', methods=['DELETE'])
@auth_required
def delete_user_watchlist(token_info, watchlist_id):
    my_watchlist = None
    for watchlist in watchlists:
        if watchlist['id'] == watchlist_id:
            my_watchlist = watchlist
            break
    if not my_watchlist:
        return jsonify({"error": f"Watchlist not found"}), 404
    user_id = my_watchlist['user_id']
    token_user_id = token_info.get('sub')
    if token_user_id != user_id:
        return jsonify({'error': "User not authorized to perform this action"}), 400
    if my_watchlist:
        # Remove watchlist from watchlists DB
        for watchlist in watchlists:
            if watchlist["id"] == watchlist_id:
                # Remove the dictionary from the list
                print(watchlist)
                watchlists.remove(watchlist)
                break  # Exit the loop after the first occurrence is removed
        # Remove watchlist from user's list
        user = users.get(user_id)
        if user and 'watchlists' in user:
            user['watchlists'].remove(watchlist_id)
            user[user_id] = user
            return jsonify({"message": f"Watchlist with ID {watchlist_id} has been deleted successfully."}), 200
        else:
            return jsonify({"error": f"Watchlist not found"}), 404


@lists_routes.route('/api/watchlists/<watchlist_id>', methods=['PUT'])
@auth_required
def update_watchlist_details(token_info, watchlist_id):
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


@lists_routes.route('/api/watchlists/<watchlist_id>/movies', methods=['DELETE'])
@auth_required
def delete_movie_from_watchlist(token_info, watchlist_id):
    data = request.json()
    if 'movie_id' not in data:
        return jsonify({"error": "No movie id provided in the request"}), 400
    movie_id = data['movie_id']
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


@lists_routes.route('/api/watchlists/<watchlist_id>/movies', methods=['PUT'])
@auth_required
def add_movie_to_watchlist(token_info, watchlist_id):
    data = request.json()
    if 'movie_id' not in data:
        return jsonify({"error": "No movie id provided in the request"}), 400
    movie_id = data['movie_id']
    watchlist = watchlists.get(watchlist_id)
    if not watchlist:
        return jsonify({"error": "Watchlist not found"}), 404
    user_id = watchlist['user_id']
    token_user_id = token_info.get('sub')
    # Make sure that the watchlist belongs to the currently logged-in user
    if token_user_id != user_id:
        return jsonify({'error': f"the watchlist does not belong to the currently logged-in user"}), 400
    watchlist['movies'].append(movie_id)
    watchlists[watchlist] = watchlist
    return jsonify({"message": f"Movie with ID {movie_id} has been added to the watchlist"}), 200