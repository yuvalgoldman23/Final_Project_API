from flask import Blueprint, request, jsonify
from auth import auth_required

feed_routes = Blueprint('feed_routes', __name__)


@feed_routes.route('/api/posts', methods=['POST'])
@auth_required
def create_post(token_info):
    data = request.json
    user_id = token_info.get('sub')
    # Basic input validation
    if 'text' not in data or 'mentioned_id' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    # Create post object
    new_post = {
        "text": data['text'],
        "mentioned_id": data['mentioned_id'],
        "user_id": user_id
    }
    # Save post to database or perform further actions
    # For demonstration, just append to posts list
    posts.append(new_post)

    return jsonify(new_post), 201


@feed_routes.route('/api/posts', methods=['GET'])
def load_last_20_posts():
    # Dummy implementation to return last 20 posts
    # Replace this with actual implementation to fetch posts from database
    return jsonify({"posts": posts[-20:]}), 200


@feed_routes.route('/api/posts/<post_id>/mention', methods=['GET'])
def get_mentioned_content_id(post_id):
    # Dummy implementation to return mentioned content ID from a post
    # TODO Replace this with actual implementation to fetch mentioned content ID from database
    # Assuming mentioned content ID is fetched based on post ID
    mentioned_content_id = "movie_123"
    return jsonify({"mentioned_content_id": mentioned_content_id}), 200


@feed_routes.route('/api/posts/mentions/<content_id>', methods=['GET'])
def get_last_20_posts_mentioning_content_id(content_id):
    # Dummy implementation to return last 20 posts mentioning a specific content ID
    # TODO Replace this with actual implementation to fetch posts from database
    last_20_posts_mentioning_content_id = [
        {"id": "789", "text": "Post mentioning content ID.", "user_id": "123"},
        {"id": "790", "text": "Another post mentioning content ID.", "user_id": "456"}
        # Add more posts here if available
    ]
    return jsonify({"posts": last_20_posts_mentioning_content_id}), 200
