import asyncio

from flask import Blueprint, jsonify, session
from auth import auth_required
from services.user_services import login_google, get_user_details
from routes.ratings_routes import get_ratings_list_data
from routes.watchlist_routes import get_main_watchlist_data
from routes.streaming_providers_routes import get_streaming_recommendation_data

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/api/login', methods=['POST', 'OPTIONS'])
@auth_required
def login(token_info):
    user_id = token_info.get('sub')
    user_email = token_info.get('email')

    return_val, status = login_google(user_id, user_email)
    if status != 200:
        return jsonify({"Error": str(return_val)}), status
    elif status == 200:
        # Store user_id in session upon successful login
        session['user_id'] = user_id
        ratings_list, status = get_ratings_list_data(user_id)
        if status != 200:
            ratings_list = []
        main_watchlist_data, status = get_main_watchlist_data(user_id)
        if status != 200:
            main_watchlist_data = None
        watchlist_streaming_data, status = asyncio.run(get_streaming_recommendation_data(watchlist_id=return_val))
        if status != 200:
            watchlist_streaming_data = None
        return jsonify({'main_watchlist_id': return_val, "main_watchlist": {"Content": main_watchlist_data, "ID":  return_val}, "ratings_list": ratings_list, "watchlist_streaming_data": watchlist_streaming_data}), 200

@user_routes.route('/api/user', methods=['GET'])
@auth_required
def get_user_details_route(token_info):
    user_id = token_info.get('sub')
    return get_user_details(user_id)

# Endpoint to check if the user is logged in
@user_routes.route('/api/is_logged_in', methods=['GET'])
def is_logged_in():
    if 'user_id' in session:
        return jsonify({'logged_in': True}), 200
    return jsonify({'logged_in': False}), 200

# New logout endpoint to delete the session
@user_routes.route('/api/logout', methods=['POST'])
def logout():
    # Remove the 'user_id' from the session to log out the user
    session.pop('user_id', None)
    print("session after logging out", session.get('user_id'))
    return jsonify({'message': 'Logged out successfully'}), 200
