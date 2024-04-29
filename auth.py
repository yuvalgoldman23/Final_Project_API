from functools import wraps
import jwt
from flask import request, jsonify, Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


# Decorator to protect API endpoints
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if the request contains an access token in the Authorization header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # Decode and verify the access token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['user']  # Extract user information from the token
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        # Pass the current user to the protected endpoint
        return f(current_user, *args, **kwargs)

    return decorated
