# routes/user_routes.py

from flask import Blueprint, request, jsonify
from auth import auth_required
from services.user_services import login_google, get_user_details
user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/api/login', methods=['POST'])
@auth_required
def login(token_info):
    user_id = token_info.get('sub')
    user_email = token_info.get('email')
    '''if user_id not in users:
        # Create a new user entry for the logged in user, including his id and username
        # TODO currently a user's DB entry only includes his ID (and potentially his watchlist IDs) - add fields, if needed'''
    # Return statement as returned from the DB
    return jsonify(login_google(user_id, user_email)), 200

@user_routes.route('/api/user', methods=['GET'])
@auth_required
def get_user_details(token_info):
    user_id = token_info.get('sub')
    # Return statement as returned from the DB
    return get_user_details(user_id)