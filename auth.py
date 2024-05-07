from functools import wraps
from flask import request, jsonify, Flask
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


# Function to verify Google OAuth2 token
def verify_google_token(token):
    token_info_endpoint = 'https://oauth2.googleapis.com/tokeninfo'
    response = requests.get(token_info_endpoint, params={'access_token': token})

    if response.status_code == 200:
        token_info = response.json()
        if not token_info.get('error'):
            return token_info
    return None


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

        # Verify Google OAuth2 token
        token_info = verify_google_token(token)
        if not token_info or not token_info.get('sub'):
            return jsonify({'message': 'Token is invalid or verification failed'}), 401
        # Pass the token info to the protected endpoint
        return f(token_info, *args, **kwargs)

    return decorated