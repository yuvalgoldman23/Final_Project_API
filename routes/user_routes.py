import asyncio

from flask import Blueprint, jsonify, request

from auth import auth_required
from routes.ratings_routes import get_ratings_list_data
from routes.watchlist_routes import get_main_watchlist_data
from services.user_services import login_google, get_user_details, update_user_region, get_user_region_db

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
        '''# Store user_id in session upon successful login
        session['user_id'] = user_id'''
        ratings_list, status = get_ratings_list_data(user_id)
        if status != 200:
            ratings_list = []
        main_watchlist_data, status = get_main_watchlist_data(user_id)
        if status != 200:
            main_watchlist_data = None
        region, status = get_user_region_db(user_id)
        # If no region is returned due a DB issue, return a default region of "US"
        if status != 200:
            region = "US"
        return jsonify({'main_watchlist_id': return_val, "main_watchlist": {"Content": main_watchlist_data, "ID":  return_val},
                        "ratings_list": ratings_list, "region": region}), 200

@user_routes.route('/api/user', methods=['GET'])
@auth_required
def get_user_details_route(token_info):
    user_id = token_info.get('sub')
    return get_user_details(user_id)


@user_routes.route('/api/user/region', methods=['GET'])
@auth_required
def get_region(token_info):
    user_id = token_info.get('sub')
    db_return_val, status = get_user_region_db(user_id)
    if status != 200:
        return jsonify({"Error": str(db_return_val)}), status
    else:
        return jsonify({'region': db_return_val}), 200


@user_routes.route('/api/user/region', methods=['POST'])
@auth_required
def update_region(token_info):
    user_id = token_info.get('sub')
    data = request.json
    print("data is " , data)
    if not data.get("region"):
        return jsonify({"Error": str(data)}), 404
    else:
        db_return_val = update_user_region(user_id, data.get("region"))
        if db_return_val != 200:
            print("Error updating region" , str(db_return_val))
            return jsonify({"Error": str(db_return_val)}), 404
        else:
            print("new region" , data.get("region"))
            return jsonify({"region": data.get("region")}), 200




'''# Endpoint to check if the user is logged in
@user_routes.route('/api/is_logged_in', methods=['GET'])
def is_logged_in():
    if 'user_id' in session:
        return jsonify({'logged_in': True}), 200
    return jsonify({'logged_in': False}), 200'''

'''
# New logout endpoint to delete the session
@user_routes.route('/api/logout', methods=['POST'])
def logout():
    # Remove the 'user_id' from the session to log out the user
    session.pop('user_id', None)
    print("session after logging out", session.get('user_id'))
    return jsonify({'message': 'Logged out successfully'}), 200'''
