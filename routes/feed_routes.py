from flask import Blueprint, request, jsonify
from auth import auth_required
import datetime

feed_routes = Blueprint('feed_routes', __name__)


def validate_user_post(post, token_id):
    if post['user_id'] != token_id:
        return jsonify({'error': f"the post does not belong to the currently logged-in user"}), 400
    else:
        return True


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
        "user_id": user_id,
        "created_at": datetime.datetime.now(),
        "post_id": len(posts) + 1
    }
    # Save post to database or perform further actions
    # For demonstration, just append to posts list
    posts.append(new_post)
    # TODO should post IDs be added to a user's DB? if so then add it here, and make sure to update accordingly at removal too

    return jsonify(new_post), 201


@feed_routes.route('/api/posts/<post_id>', methods=['DELETE'])
@auth_required
def delete_post(token_info, post_id):
    user_id = token_info.get('sub')
    # Find post in DB
    my_post = None
    for post in posts:
        if post['post_id'] == post_id:
            my_post = post
            break
    if not my_post:
        return jsonify({'error': f"the post id provided doesn't exist"}), 400
    elif validate_user_post(my_post, user_id):
        posts.remove(my_post)
        # TODO reload posts on client  side?
        return jsonify({'success': f"post deleted successfully"}), 201


@feed_routes.route('/api/posts/<post_id>', methods=['PUT'])
@auth_required
def edit_post(token_info, post_id):
    data = request.json
    user_id = token_info.get('sub')

    # Find post in DB
    for post in posts:
        if post['post_id'] == post_id:
            if not validate_user_post(post, user_id):
                break
            # Update post content if data contains a value for it
            if 'text' in data:
                post['text'] = data['text']
            if 'content_id' in data:
                post['content_id'] = data['content_id']
            # TODO - ADD 'update_date' field to the post???
            # TODO: Reload posts on the client side if needed
            # Return the newly edited post
            return jsonify({'post': post, 'success': f"post updated successfully"}), 201
    # If reached here, post not found, thus return an error
    return jsonify({'error': f"the post id provided doesn't exist"}), 400


@feed_routes.route('/api/posts', methods=['GET'])
def load_last_20_posts():
    # Dummy implementation to return last 20 posts
    # Replace this with actual implementation to fetch posts from database
    return jsonify({"posts": posts[-20:]}), 200


# TODO probably not needed, the client could just send the server that content id instead, in order to load its page
@feed_routes.route('/api/posts/<post_id>/mention', methods=['GET'])
def get_mentioned_content_id(post_id):
    # Dummy implementation to return mentioned content ID from a post
    # TODO Replace this with actual implementation to fetch mentioned content ID from database
    # Assuming mentioned content ID is fetched based on post ID
    mentioned_content_id = "movie_123"
    return jsonify({"mentioned_content_id": mentioned_content_id}), 200


# Return the 20 last posts mentioning a certain content id
# To be used for content pages, displaying "their own feed" solely centred on the content
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
