from functools import wraps
from flask import request, jsonify, Flask, session
import requests

app = Flask(__name__)

# Function to verify Google OAuth2 token
def verify_google_token(token):
    token_info_endpoint = 'https://oauth2.googleapis.com/tokeninfo'
    response = requests.get(token_info_endpoint, params={'access_token': token})

    if response.status_code == 200:
        token_info = response.json()
        if not token_info.get('error'):
            return token_info
    return None


# Decorator to protect API endpoints and check login
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Check if user is already logged in by checking session
        if 'user_id' in session:
            # Optionally, re-validate token to ensure it hasn't expired
            token = session.get('token')
            if token:
                token_info = verify_google_token(token)
                if not token_info or not token_info.get('sub'):
                    # Token is invalid or expired, clear the session
                    session.clear()
                    return jsonify({'message': 'Session expired. Please log in again.'}), 401
                # Token is still valid, proceed
                return f(token_info, *args, **kwargs)

        # If not logged in, check token in Authorization header
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        # Verify Google OAuth2 token
        token_info = verify_google_token(token)
        if not token_info or not token_info.get('sub'):
            return jsonify({'message': 'Token is invalid or verification failed'}), 401

        '''# Store user ID (sub) and token in session
        session['user_id'] = token_info['sub']
        session['token'] = token  # Store token for further checks'''

        # Pass the user ID to the protected endpoint
        return f(token_info, *args, **kwargs)

    return decorated

if __name__ == '__main__':
    app.run(debug=True)
