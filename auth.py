from functools import wraps
from flask import request, jsonify
from basic_server_user_api import google


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        # Assuming AuthJS validates the token and returns the user_id if valid, None otherwise
        # TODO find out how to perform this validation and access of user_id
        user_id = google.validate_token(token)
        if not user_id:
            return jsonify({"error": "Invalid token"}), 401
        # Check if the user_id from the token matches the user_id from the route
        if str(user_id) != str(kwargs['user_id']):
            return jsonify({"error": "Token does not match user_id"}), 401
        # If token is valid and matches the user_id, continue with the request
        return f(*args, **kwargs)

    return decorated_function
