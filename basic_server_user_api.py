from flask import Flask, request, jsonify, url_for, redirect, session, abort
from urllib.parse import urlencode
from dotenv import load_dotenv
from auth import auth_required
import jwt
import requests
import os
import secrets

app = Flask(__name__)

# Dummy database for storing user data
users = {"1": {
    "id": "1",
    "username": "john_doe",
    "email": "john.doe@example.com",
    "password": "hashed_password",
    "name": "John Doe",
    "profile_pic": "https://example.com/profile_pic.jpg",
    "other_details": {
        "age": 30,
        "location": "New York"
    }
}}

# Dummy database for storing watchlists
watchlists = {}

# Dummy database for storing posts
posts = {}

# TODO add function to validate email format, password strength, etc

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
        'user_id': provider_data['userinfo']['user_id'](response.json())
    }

    # TODO add a check if the user already exists in our DB
    # TODO if exists, retrieve the user's content and send to client
    # TODO if user doesn't exist, create a new DB entry with the user's info

    # Perform actions if valid
    if user_info['name'] and user_info['email'] and user_info['user_id']:
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


@app.route('/api/watchlists', methods=['POST'])
@auth_required
def create_watchlist():
    data = request.json
    # Basic input validation
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id field"}), 400
    # TODO - limit the number of watchlists per user???
    user_id = data['user_id']
    # TODO add a check for name length? probably more fitting to do in the client
    name = data.get('name', 'Untitled Watchlist')
    description = data.get('description', '')
    # Check if user exists
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    # Generate watchlist ID
    watchlist_id = str(len(watchlists) + 1)
    # Create watchlist object
    new_watchlist = {
        "id": watchlist_id,
        "user_id": user_id,
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
    users[user_id] = user

    return jsonify(new_watchlist), 201


@app.route('/api/watchlists/<watchlist_id>', methods=['GET'])
# @auth_required
def get_watchlist(watchlist_id):
    watchlist = watchlists.get(watchlist_id)
    data = request.json
    # TODO - should watchlists be public? if so, no token or auth required....
    # TODO add token check
    if watchlist:
        return jsonify(watchlist)
    else:
        return jsonify({"error": "Watchlist not found"}), 404


# TODO change/add to this so it only returns results for the currently logged in user??


@app.route('/api/users/<user_id>/watchlists', methods=['GET'])
# @auth_required
def get_user_watchlists(user_id):
    data = request.json
    # Check that the user actually exists...
    user = users.get(user_id)
    if user:
        user_watchlist_ids = user.get('watchlists', [])
        user_watchlists = [watchlists[watchlist_id] for watchlist_id in user_watchlist_ids]
        return jsonify(user_watchlists)
    else:
        return jsonify({"error": "User not found"}), 404


# TODO after finishing the Movies API, add a method to convert a watchlist's movie id's to a list of movie details?


@app.route('/api/watchlists/<watchlist_id>', methods=['DELETE'])
# @auth_required
def delete_user_watchlist(watchlist_id):
    watchlist = watchlists.get(watchlist_id)
    if watchlist:
        # Remove watchlist from watchlists DB
        del watchlists[watchlist_id]
        # Remove watchlist from user's list
        user_id = watchlist['user_id']
        user = users.get(user_id)
        if user and 'watchlists' in user:
            user['watchlists'].remove(watchlist_id)
            user[user_id] = user
            return jsonify({"message": f"Watchlist with ID {watchlist_id} has been deleted successfully."}), 200
        else:
            return jsonify({"error": f"Watchlist not found"}), 404


@app.route('/api/watchlists/<watchlist_id>', methods=['PUT'])
# @auth_required
def update_watchlist(watchlist_id):
    data = request.json
    watchlist = watchlists.get(watchlist_id)
    if watchlist:
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


@app.route('/api/watchlists/<watchlist_id>/movies/<movie_id>', methods=['DELETE'])
# @auth_required
def delete_movie_from_watchlist(watchlist_id, movie_id):
    data = request.json
    watchlist = watchlists.get(watchlist_id)
    if not watchlist:
        return jsonify({"error": "Watchlist not found"}), 404
    # Check if movie exists in the watchlist
    for movie in watchlist['movies']:
        if movie['id'] == movie_id:
            # Delete the movie from the watchlist
            watchlist['movies'].remove(movie)
            # Save updated watchlist to database
            watchlists[watchlist_id] = watchlist
            return jsonify({"message": f"Movie with ID {movie_id} has been deleted from the watchlist"}), 200

    return jsonify({"error": f"Movie with ID {movie_id} not found in the watchlist"}), 404


@app.route('/api/posts', methods=['POST'])
# @auth_required
def create_post():
    data = request.json
    # Basic input validation
    if not all(key in data for key in ('text', 'user_id', 'token')):
        return jsonify({"error": "Missing required fields"}), 400
    # Create post object
    new_post = {
        "text": data['text'],
        "mentioned_user_id": data.get('mentioned_user_id'),
        "user_id": data['user_id']
    }
    # Save post to database or perform further actions
    # For demonstration, just append to posts list
    posts.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts', methods=['GET'])
def load_last_20_posts():
    # Dummy implementation to return last 20 posts
    # Replace this with actual implementation to fetch posts from database
    return jsonify({"posts": posts[-20:]}), 200


@app.route('/api/posts/<post_id>/mention', methods=['GET'])
def get_mentioned_content_id(post_id):
    # Dummy implementation to return mentioned content ID from a post
    # TODO Replace this with actual implementation to fetch mentioned content ID from database
    # Assuming mentioned content ID is fetched based on post ID
    mentioned_content_id = "movie_123"
    return jsonify({"mentioned_content_id": mentioned_content_id}), 200


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
TMDB_API_KEY = "YOUR_TMDB_API_KEY"


@app.route('/api/streaming-providers', methods=['GET'])
def get_streaming_providers():
    content_id = request.args.get('content_id')
    territory = request.args.get('territory')
    # Content type is 'tv' or 'movie'
    content_type = request.args.get('content_type')
    if not content_id or not territory:
        return jsonify({"error": "Content ID and territory are required"}), 400

    # Fetch streaming providers from TMDB
    tmdb_url = f"https://api.themoviedb.org/3/{content_type}/{content_id}/watch/providers"
    headers = {
        "Authorization": f"Bearer {TMDB_API_KEY}",
        "accept": "application/json"
    }
    params = {
        "territory": territory
    }

    try:
        response = requests.get(tmdb_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        streaming_providers = data.get("results", {}).get(territory, {}).get("flatrate", [])
        provider_names = [provider.get("provider_name") for provider in streaming_providers]
        return jsonify({"streaming_providers": provider_names}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


# TODO - add an endpoint that returns the logo of a streaming provider?


if __name__ == '__main__':
    app.run(debug=True)
