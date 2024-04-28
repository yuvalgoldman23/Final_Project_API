from flask import Flask, request, jsonify, url_for, redirect, session
from authlib.integrations.flask_client import OAuth
from auth import auth_required
import requests

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

# Configure OAuth
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key='your_google_client_id',
    consumer_secret='your_google_client_secret',
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


# API endpoints


@app.route('/')
def index():
    return 'Placeholder'


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason={}, error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (resp['access_token'], '')
    # Call your callback function here
    return callback()


# OAuth Callback Route
@app.route('/callback')
def callback():
    token = session.get('google_token')
    if not token:
        return 'Access denied: Missing access token'
    # Use the token to authenticate the user, extract user information, etc.
    # Retrieve user information from AuthJS userinfo endpoint
    user_info = google.get('userinfo').json()
    user_id = user_info.get('sub')
    user_name = user_info.get('name')
    user_pic = user_info.get('picture')
    # Authenticate the user and establish a session
    # Return a json including redirection to the index, the authjs token, and some user info
    return jsonify({'redirect_url': url_for('index'), 'token': token[0], 'user_id': user_id,
                    'user_name': user_name, 'user_pic': user_pic})


# Login Route - Redirect to AuthJS Authorization Endpoint
@app.route('/login')
def login():
    # Upon authorization, redirect to callback so the needed details are then transferred back to the client
    return oauth.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    # Clear the session data to log out the user
    session.clear()
    return jsonify({'message': 'Logged out successfully'})


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
@auth_required
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
@auth_required
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
@auth_required
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


@app.route('api/watchlists/<watchlist_id', method=['PUT'])
@auth_required
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
@auth_required
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
@auth_required
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
