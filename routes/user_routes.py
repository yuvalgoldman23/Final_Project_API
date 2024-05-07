# routes/user_routes.py

from flask import Blueprint, request, jsonify
from auth import auth_required

user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/api/login', methods=['POST'])
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
