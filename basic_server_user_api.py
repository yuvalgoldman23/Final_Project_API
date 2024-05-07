from flask import Flask, request, jsonify, url_for, redirect, session, abort
from urllib.parse import urlencode
from dotenv import load_dotenv
from auth import auth_required
import requests
import os
import secrets
import datetime

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Dummy database for storing user data
users = {"113749586527602021810": {
    "id": "113749586527602021810",
    "username": "john_doe",
}
}

# Dummy database for storing watchlists
watchlists = [{'id': '1', 'user_id': '12', 'name': 'testing'}]

# Dummy database for storing posts
posts = []

# OAuth Implementation

app.config['SECRET_KEY'] = 'top secret!'
app.config['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET')
app.config['GOOGLE_AUTHORIZE_URL'] = 'https://accounts.google.com/o/oauth2/auth'
app.config['GOOGLE_TOKEN_URL'] = 'https://oauth2.googleapis.com/token'
app.config['GOOGLE_USERINFO_URL'] = 'https://www.googleapis.com/oauth2/v3/userinfo'
app.config['GOOGLE_SCOPES'] = ['https://www.googleapis.com/auth/userinfo.email',
                               'https://www.googleapis.com/auth/userinfo.profile']


@app.route("/")
def home():
    return redirect(url_for('oauth2_authorize'))


@app.route("/callback")
def callback():
    provider_data = {
        'client_id': app.config['GOOGLE_CLIENT_ID'],
        'client_secret': app.config['GOOGLE_CLIENT_SECRET'],
        'token_url': app.config['GOOGLE_TOKEN_URL'],
        'userinfo': {
            'url': app.config['GOOGLE_USERINFO_URL'],
            'name': lambda json: json['name'],
            'email': lambda json: json['email'],
            'user_id': lambda json: json['sub'],
        },
    }

    # Make sure that the state parameter matches the one we created in the authorization request
    if request.args['state'] != session.get('oauth2_state'):
        abort(401)

    # Make sure that the authorization code is present
    if 'code' not in request.args:
        abort(401)

    # Exchange the authorization code for an access token
    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('callback', _external=True),
    }, headers={'Accept': 'application/json'})

    if response.status_code != 200:
        abort(401)

    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        abort(401)

    # Use the access token to get the user's email address
    response = requests.get(provider_data['userinfo']['url'], headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })

    if response.status_code != 200:
        abort(401)

    user_info = {
        'name': provider_data['userinfo']['name'](response.json()),
        'email': provider_data['userinfo']['email'](response.json()),
        'user_id': provider_data['userinfo']['user_id'](response.json()),
        'token': oauth2_token
    }

    # TODO add a check if the user already exists in our DB
    # TODO if exists, retrieve the user's content and send to client
    # TODO if user doesn't exist, create a new DB entry with the user's info

    # Perform actions if valid
    if user_info['name'] and user_info['email'] and user_info['user_id'] and oauth2_token:
        return jsonify(user_info)
    else:
        return "Failed to fetch user information"


@app.route('/authorize')
def oauth2_authorize():
    # generate a random string for the state parameter
    session['oauth2_state'] = secrets.token_urlsafe(16)

    # create a query string with all the OAuth2 parameters
    qs = urlencode({
        'client_id': app.config['GOOGLE_CLIENT_ID'],
        'redirect_uri': url_for('callback', _external=True),
        'response_type': 'code',
        'scope': ' '.join(app.config['GOOGLE_SCOPES']),
        'state': session['oauth2_state'],
    })

    # redirect the user to the Google OAuth2 provider authorization URL
    return redirect(app.config['GOOGLE_AUTHORIZE_URL'] + '?' + qs)


@app.route('/api/login', methods=['POST'])
@auth_required
def create_new_user(token_info):
    user_id = token_info.get('sub')
    if user_id not in users:
        # Create a new user entry for the logged in user, including his id and username
        # TODO currently dummy, replace with true DB implementation upon completion
        # TODO currently a user's DB entry only includes his ID (and potentially his watchlist IDs) - add fields, if needed
        users[user_id] = {'id': user_id}
        return jsonify({"success": f"New user created"}), 200
    return jsonify({"success": "Existing user logged in"}), 200


# TODO create a new user endpoint - whether an api endpoint or a transparent function that only runs if the user isn't known to us

@app.route('/api/watchlists', methods=['POST'])
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
    watchlists.append(new_watchlist)
    # TODO - decide how watchlists are saved
    #  currently we have a watchlists DB, and each user has a field with their watchlists ids
    # Update user's watchlist IDs
    user.setdefault('watchlists', []).append(watchlist_id)
    users[token_user_id] = user
    print(users)
    return jsonify(new_watchlist), 201


@app.route('/api/watchlists/<watchlist_id>', methods=['GET'])
@auth_required
def get_watchlist(token_info, watchlist_id):
    # PLACEHOLDER until DB implementation and queries
    my_watchlist = None
    for watchlist in watchlists:
        if watchlist['id'] == watchlist_id:
            my_watchlist = watchlist
            break
    # TODO - should watchlists be public? if so, no token or auth required....
    if my_watchlist:
        return jsonify(my_watchlist)
    else:
        return jsonify({"error": "Watchlist not found"}), 404


# TODO change/add to this so it only returns results for the currently logged in user??


@app.route('/api/users/watchlists', methods=['GET'])
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


@app.route('/api/watchlists/<watchlist_id>', methods=['DELETE'])
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


@app.route('/api/watchlists/<watchlist_id>', methods=['PUT'])
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


@app.route('/api/watchlists/<watchlist_id>/movies', methods=['DELETE'])
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


def validate_user_post(post, token_id):
    if post['user_id'] != token_id:
        return jsonify({'error': f"the post does not belong to the currently logged-in user"}), 400
    else:
        return True


@app.route('/api/posts', methods=['POST'])
@auth_required
def create_post(token_info):
    data = request.json
    user_id = token_info.get('sub')
    # Basic input validation
    if 'text' not in data or 'mentioned_id' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    # Create post object
    new_post = {
        "text": data['text'],
        "mentioned_id": data['mentioned_id'],
        "user_id": user_id,
        "created_at": datetime.datetime.now(),
        "post_id": len(posts) + 1
    }
    # Save post to database or perform further actions
    # For demonstration, just append to posts list
    posts.append(new_post)
    # TODO should post IDs be added to a user's DB? if so then add it here, and make sure to update accordingly at removal too

    return jsonify(new_post), 201


@app.route('/api/posts/<post_id>', methods=['DELETE'])
@auth_required
def delete_post(token_info, post_id):
    user_id = token_info.get('sub')
    # Find post in DB
    my_post = None
    for post in posts:
        if post['post_id'] == post_id:
            my_post = post
            break
    if not my_post:
        return jsonify({'error': f"the post id provided doesn't exist"}), 400
    else:
        if my_post['user_id'] != user_id:
            return jsonify({'error': f"the post does not belong to the currently logged-in user"}), 400
        else:
            posts.remove(my_post)
            # TODO reload posts on client  side?
            return jsonify({'success': f"post deleted successfully"}), 201


@app.route('/api/posts/<post_id>', methods=['PUT'])
@auth_required
def edit_post(token_info, post_id):
    data = request.json
    user_id = token_info.get('sub')

    # Find post in DB
    for post in posts:
        if post['post_id'] == post_id:
            if not validate_user_post(post, user_id):
                break
            # Update post content if data contains a value for it
            if 'text' in data:
                post['text'] = data['text']
            if 'content_id' in data:
                post['content_id'] = data['content_id']
            # TODO - ADD 'update_date' field to the post???
            # TODO: Reload posts on the client side if needed
            # Return the newly edited post
            return jsonify({'post': post, 'success': f"post updated successfully"}), 201
    # If reached here, post not found, thus return an error
    return jsonify({'error': f"the post id provided doesn't exist"}), 400


@app.route('/api/posts', methods=['GET'])
def load_last_20_posts():
    # Dummy implementation to return last 20 posts
    # Replace this with actual implementation to fetch posts from database
    return jsonify({"posts": posts[-20:]}), 200


# TODO probably not needed, the client could just send the server that content id instead, in order to load its page
@app.route('/api/posts/<post_id>/mention', methods=['GET'])
def get_mentioned_content_id(post_id):
    # Dummy implementation to return mentioned content ID from a post
    # TODO Replace this with actual implementation to fetch mentioned content ID from database
    # Assuming mentioned content ID is fetched based on post ID
    mentioned_content_id = "movie_123"
    return jsonify({"mentioned_content_id": mentioned_content_id}), 200


# Return the 20 last posts mentioning a certain content id
# To be used for content pages, displaying "their own feed" solely centred on the content
@app.route('/api/posts/mentions/<content_id>', methods=['GET'])
def get_last_20_posts_mentioning_content_id(content_id):
    # Dummy implementation to return last 20 posts mentioning a specific content ID
    # TODO Replace this with actual implementation to fetch posts from database
    last_20_posts_mentioning_content_id = [
        {"id": "789", "text": "Post mentioning content ID.", "user_id": "123"},
        {"id": "790", "text": "Another post mentioning content ID.", "user_id": "456"}
        # Add more posts here if available
    ]
    return jsonify({"posts": last_20_posts_mentioning_content_id}), 200


# TODO Replace with your TMDB API key
TMDB_API_KEY = 'f3ca6c11eaf43465a1814fa3a2440f37'


# TODO remove territory from this request?
@app.route('/api/streaming-providers', methods=['GET'])
def get_streaming_providers():
    content_id = request.args.get('content_id')
    territory = request.args.get('territory', None)
    # Content type is 'tv' or 'movie'
    content_type = request.args.get('content_type')
    if not content_id:
        return jsonify({"error": "Content ID and territory are required"}), 400
    # Fetch streaming providers from TMDB
    tmdb_url = f"https://api.themoviedb.org/3/{content_type}/{content_id}/watch/providers"
    headers = {
        "api_key": f"{TMDB_API_KEY}",
        "accept": "application/json"
    }
    params = {"api_key": TMDB_API_KEY}
    try:
        response = requests.get(tmdb_url, params=params)
        response.raise_for_status()
        data = response.json()
        # 'flatrate' means "available on streaming"
        streaming_providers = data.get("results", {}).get(territory, {}).get("flatrate", [])
        # TODO - think about what to return if streaming_providers== None due to no flatrate available
        provider_info = [
            {
                "name": provider.get("provider_name"),
                "logo_path": provider.get("logo_path"),
                "provider_id": provider.get("provider_id"),
                "display_priority": provider.get("display_priority")
            }
            for provider in streaming_providers
        ]
        # todo return logo for a provider or let a different API endpoint do that from our local DB?
        return jsonify({"providers": provider_info}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


# TODO - add an endpoint that returns the logo of a streaming provider?


if __name__ == '__main__':
    app.run(debug=False)