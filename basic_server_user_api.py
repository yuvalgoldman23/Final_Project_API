from flask import Flask, request, jsonify
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


# API endpoints

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json

    # Basic input validation
    if not all(key in data for key in ('username', 'email', 'password')):
        return jsonify({"error": "Missing required fields"}), 400
    # TODO add a check for username length - probably more fitting to do in the client
    username = data['username']
    email = data['email']
    password = data['password']

    # Check if username or email already exists
    for user in users.values():
        if user['username'] == username:
            return jsonify({"error": "Username already exists"}), 409
        if user['email'] == email:
            return jsonify({"error": "Email already exists"}), 409

    # Generate user ID
    user_id = str(len(users) + 1)

    # Create user object
    new_user = {
        "id": user_id,
        "username": username,
        "email": email,
        "password": password  # Note: In a real application, password should be securely hashed before saving
    }

    # Save user to database
    users[user_id] = new_user

    return jsonify(new_user), 201


@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/api/users/<user_id>/details', methods=['PUT'])
def update_user_details(user_id):
    user = users.get(user_id)
    if user:
        update_data = request.json

        # Check if 'username' is present in the update_data
        if 'username' in update_data:
            return jsonify({"error": "Username cannot be updated"}), 400

        # Update other details
        user.update(update_data)
        users[user_id] = user
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({"message": f"User with ID {user_id} has been deleted successfully."})
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/api/users', methods=['GET'])
def list_users():
    return jsonify(list(users.values()))


@app.route('/api/login', methods=['POST'])
def user_login():
    credentials = request.json
    for user in users.values():
        if user['email'] == credentials['email'] and user['password'] == credentials['password']:
            return jsonify({"token": "dummy_token"}), 200
    return jsonify({"error": "Invalid credentials"}), 401


@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    email = request.json.get('email')
    # Logic for sending password reset email
    return jsonify({"message": "Password reset email sent successfully."}), 200


@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    reset_data = request.json
    # Logic for resetting password
    return jsonify({"message": "Password reset successful."}), 200


@app.route('/api/users/<user_id>/details', methods=['GET'])
def get_user_details(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/api/users/<user_id>/details', methods=['PUT'])
def update_user_details(user_id):
    user = users.get(user_id)
    if user:
        update_data = request.json
        user.update(update_data)
        users[user_id] = user
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/api/watchlists', methods=['POST'])
def create_watchlist():
    data = request.json
    # Basic input validation
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id field"}), 400
    if 'token' not in data:
        return jsonify({"error": "Missing token field"}), 400
    # TODO - limit the number of watchlists per user???
    user_id = data['user_id']
    token = data['token']
    # TODO add a check for name length? probably more fitting to do in the client
    name = data.get('name', 'Untitled Watchlist')
    description = data.get('description', '')
    # Check if user exists
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    # TODO check user token - add usage of OAuth here
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
def get_watchlist(watchlist_id):
    watchlist = watchlists.get(watchlist_id)
    data = request.json
    if 'token' not in data:
        return jsonify({"error": "Missing token field"}), 400
    token = data['token']
    # TODO add token check
    if watchlist:
        return jsonify(watchlist)
    else:
        return jsonify({"error": "Watchlist not found"}), 404


# TODO change/add to this so it only returns results for the currently logged in user??


@app.route('/api/users/<user_id>/watchlists', methods=['GET'])
def get_user_watchlists(user_id):
    data = request.json
    if 'token' not in data:
        return jsonify({"error": "Missing token field"}), 400
    user = users.get(user_id)
    # TODO add token check for user
    if user:
        user_watchlist_ids = user.get('watchlists', [])
        user_watchlists = [watchlists[watchlist_id] for watchlist_id in user_watchlist_ids]
        return jsonify(user_watchlists)
    else:
        return jsonify({"error": "User not found"}), 404


# TODO after finishing the Movies API, add a method to convert a watchlist's movie id's to a list of movie details?


@app.route('/api/watchlists/<watchlist_id>', methods=['DELETE'])
def delete_user_watchlist(watchlist_id):
    data = request.json
    if 'token' not in data:
        return jsonify({"error": "Missing token field"}), 400
    watchlist = watchlists.get(watchlist_id)
    # TODO add step to check token validity compared to user_id
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
def update_watchlist(watchlist_id):
    data = request.json
    if 'token' not in data:
        return jsonify({"error": "Missing token field"}), 400
    # TODO add step to check token validity compared to user_id in the watchlist
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
def delete_movie_from_watchlist(watchlist_id, movie_id):
    data = request.json
    if 'token' not in data:
        return jsonify({"error": "Missing token field"}), 400
    watchlist = watchlists.get(watchlist_id)
    # TODO add validation of token compared to the user_id in the watchlist
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
def create_post():
    data = request.json

    # Basic input validation
    if not all(key in data for key in ('text', 'user_id', 'token')):
        return jsonify({"error": "Missing required fields"}), 400

    # Validate user token (mocked validation for demonstration)
    if not validate_token(data['user_id'], data['token']):
        return jsonify({"error": "Invalid user token"}), 401

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


def validate_token(user_id, token):
    # Dummy token validation (replace with actual implementation)
    return True  # Always validate for demonstration purposes


if __name__ == '__main__':
    app.run(debug=True)
