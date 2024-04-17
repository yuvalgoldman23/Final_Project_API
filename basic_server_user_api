from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy database for storing user data
users = {}

# API endpoints

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json

    # Basic input validation
    if not all(key in data for key in ('username', 'email', 'password')):
        return jsonify({"error": "Missing required fields"}), 400

    username = data['username']
    email = data['email']
    password = data['password']

    # Check if username or email already exists
    for user in users.values():
        if user['username'] == username:
            return jsonify({"error": "Username already exists"}), 409
        if user['email'] == email:
            return jsonify({"error": "Email already exists"}), 409

    # Generate user ID
    user_id = str(len(users) + 1)

    # Create user object
    new_user = {
        "id": user_id,
        "username": username,
        "email": email,
        "password": password  # Note: In a real application, password should be securely hashed before saving
    }

    # Save user to database
    users[user_id] = new_user

    return jsonify(new_user), 201

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = users.get(user_id)
    if user:
        update_data = request.json
        user.update(update_data)
        users[user_id] = user
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({"message": f"User with ID {user_id} has been deleted successfully."})
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/users', methods=['GET'])
def list_users():
    return jsonify(list(users.values()))

@app.route('/api/login', methods=['POST'])
def user_login():
    credentials = request.json
    for user in users.values():
        if user['email'] == credentials['email'] and user['password'] == credentials['password']:
            return jsonify({"token": "dummy_token"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    email = request.json.get('email')
    # Logic for sending password reset email
    return jsonify({"message": "Password reset email sent successfully."}), 200

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    reset_data = request.json
    # Logic for resetting password
    return jsonify({"message": "Password reset successful."}), 200

@app.route('/api/users/<user_id>/details', methods=['GET'])
def get_user_details(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/users/<user_id>/details', methods=['PUT'])
def update_user_details(user_id):
    user = users.get(user_id)
    if user:
        update_data = request.json
        user.update(update_data)
        users[user_id] = user
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
