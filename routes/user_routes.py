from flask import Blueprint, jsonify, session
from auth import auth_required
from services.user_services import login_google, get_user_details

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
        print("session id is", session.get('user_id'))
        return jsonify({'main_watchlist_id': return_val}), 200

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
