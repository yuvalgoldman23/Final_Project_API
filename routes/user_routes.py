# routes/user_routes.py

from flask import Blueprint, request, jsonify
from auth import auth_required
from services.user_services import login_google, get_user_details
user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/api/login', methods=['POST'])
@auth_required
def login(token_info):
    # TODO add user's name to DB upon registration and send to client
    # TODO return the main watchlist for the user if already registered and also his rating and reviews lists???
    user_id = token_info.get('sub')
    user_email = token_info.get('email')
    '''if user_id not in users:
        # Create a new user entry for the logged in user, including his id and username'''
    # Return statement as returned from the DB
    return_val, status = login_google(user_id, user_email)
    if status != 200:
        return jsonify({'Error' : return_val}), status
    elif status == 200:
        # TODO add sending the username?
        return jsonify({'main_watchlist_id': return_val}), 200

@user_routes.route('/api/user', methods=['GET'])
@auth_required
def get_user_details(token_info):
    user_id = token_info.get('sub')
    # Return statement as returned from the DB
    return get_user_details(user_id)