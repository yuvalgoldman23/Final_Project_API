from flask import Blueprint, request, jsonify
from auth import auth_required
import datetime
import services.feed_services as service
from utils import isNegative
feed_routes = Blueprint('feed_routes', __name__)


# A Post could include either mentions (of other users) or hashtags (of media content)
# Both mentions and hashtags are lists (we could mention multiple people or movies - or none) - would probably be smart to limit their sizes
# A post belongs to a certain user
# A post could have other posts linked above it and below it (a parent-child relationship) as comments to a post.
# We want to be able to display all posts of a certain user (token not required)
# We want to allow a user to only edit/remove posts by himself (token required)
# We want to allow getting all posts mentioning a certain content (no token required) - later, delivery with content page?
# Fields of a post in the server side: post_id, user_id (owner), parent_post_id, child_post_id, mentions_list, hashtags_list, creation_date


def is_post_id_valid(post_id):
    return service.does_post_id_exist(post_id)


@feed_routes.route('/api/feed', methods=['POST'])
@auth_required
def add_post(token_info):
    user_id = token_info.get('sub')
    data = request.json
    text_content = data.get('text_content')
    if not text_content:
        return jsonify({'error': 'No text content provided'}), 400
    parent_id = data.get('parent_id', None)
    is_child = data.get('is_child')
    if is_child is None:
        return jsonify({'error': 'No is_child provided'}), 400
    # If the post is said to be a child, but no parent id provided, return an error
    if is_child and parent_id is None:
        return jsonify({'error': 'This is is a child post, but no parent_id was provided'}), 400
    # Check if the parent post actually exists
    if not is_post_id_valid(parent_id):
        return jsonify({'error': 'Invalid parent post id'}), 400
    mentions = data.get('mentions')
    tags = data.get('tags')
    # First create the post-entry in the DB, then later add the tags and mentions, once we have a post id
    return_val, status  = service.add_post(user_id, parent_id, is_child, text_content)
    if status != 200:
        print(return_val)
        return jsonify({'error': return_val}), status
    else:
        # Now add the tags and mentions into the DB, linked to the newly created post id
        mentions_id = []
        tags_id = []
        if mentions:
            for mention in mentions:
                new_mention = service.add_mention(return_val, mention.get('mentioned_user_id'), mention.get('start_position'), mention.get('length'))
                if not new_mention:
                    #  Remove post, since it wasn't fully created
                    service.remove_post(return_val)
                    return jsonify({'error': 'Error adding mention to post, please try sending request again'}), 400
                mentions_id.append({"mention_id": new_mention, "mentioned_user_id": mention.get("mentioned_user_id")})
        if tags:
            for tag in tags:
                new_tag = service.add_tag(return_val, tag.get('tagged_media_id'), tag.get('start_position'), tag.get('length'))
                if not new_tag:
                    #  Remove post, since it wasn't fully created
                    service.remove_post(return_val)
                    return jsonify({'error': 'Error adding tag to post, please try sending request again'}), 400
                tags_id.append({"tag_id": new_tag, "tagged_media_id": tag.get('tagged_media_id')})
        return jsonify({'post_id': return_val, 'mentions': mentions_id, 'tags': tags_id, 'is_child': is_child, 'parent_id': parent_id}), 200



@feed_routes.route('/api/feed/child_posts', methods=['GET'])
def get_child_posts():
    data = request.json
    parent_id = data.get('parent_id', None)
    if parent_id is None:
        return jsonify({'error': 'No parent_id was provided'}), 400
    if not is_post_id_valid(parent_id):
        return jsonify({'error': 'Invalid parent post id'}), 400
    requested_num_of_posts = data.get('requested_num_of_posts', None)
    if requested_num_of_posts and isNegative(requested_num_of_posts):
        return jsonify({'error': "Invalid number of posts requested"}), 400
    # If no required number of posts provided, return all of them
    db_response, status = service.get_posts_by_parentid(parent_id, requested_num_of_posts)
    if status != 200:
        return jsonify({'error': db_response}), status
    else:
        return jsonify({'posts': db_response}), 200

@feed_routes.route('/api/feed/edit_post_text', methods=['PUT'])
@auth_required
def update_post_text(token_info):
    # TODO add the ability to edit mentions and tags (add or remove) from here? Ask Omer about the most comfortable way
    user_id = token_info.get('sub')
    data = request.json
    post_id = data.get('post_id')
    if not post_id:
        return jsonify({'error': 'No post_id was provided'}), 400
    new_text = data.get('new_text')
    if not new_text:
        return jsonify({'error': 'No new text was provided'}), 400
    db_response, status = service.update_post_text(post_id, new_text, user_id)
    if status != 200:
        return jsonify({'error': db_response}), status
    else:
        return jsonify({'success': f"post {post_id} updated with new text {new_text}"}), status


@feed_routes.route('/api/feed/user')
def get_posts_by_user():
    data = request.json
    user_id = data.get('user_id')
    requested_num_of_posts = data.get('requested_num_of_posts', None)
    if requested_num_of_posts and isNegative(requested_num_of_posts):
        return jsonify({'error': "Invalid number of posts requested"}), 400
    # If no required number of posts provided, return all of them
    db_response, status = service.get_posts_by_user(user_id, requested_num_of_posts)
    if status != 200:
        return jsonify({'error': db_response}), status
    else:
        return jsonify({'user_posts': db_response, 'user_id': user_id}), status

# To be used for loading earlier posts in the feed
@feed_routes.route('/api/feed/', methods=['GET'])
def get_last_n_posts():
    data = request.json
    n = data.get('number_of_posts', None)
    if not n or isNegative(n):
        return jsonify({'error': "Invalid number of posts"}), 400
    else:
        earlier_than = data.get('earlier_than', None)
        db_response, status = service.get_last_n_posts(n, earlier_than)
        if status != 200:
            return jsonify({'error': db_response}), status
        else:
            return jsonify({'posts': db_response}), status


@feed_routes.route('/api/feed', methods=['DELETE'])
@auth_required
def delete_post(token_info):
    user_id = token_info.get('sub')
    data = request.json
    post_id = data.get('post_id', None)
    if not post_id:
        return jsonify({'error': "No post id provided"}), 400
    else:
        db_response, status = service.remove_post(post_id, user_id)
        if status != 201:
            return jsonify({'error': db_response}), status
        else:
            return jsonify({'post_id': post_id, 'success': db_response}), status




# TODO add a function to request the N posts earlier than the post created at sec:sec:min:min:hh:dd:mm:yy

# TODO FOR TESTING PURPOSES ONLY - ID RETURNED IS INCORRECT IF MANY SUCCESSIVE DB ENTRIES ARE CREATED
@feed_routes.route('/api/feed/tag', methods=['POST'])
def create_tag():
    db_res, status = service.add_tag('666', '666',  '66', '1')
    return jsonify({'new_id': db_res}), 200


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

@feed_routes.route('/api/posts/stam', methods=['GET'])
def feedstam():
    return jsonify(service.add_mention("666","66",6,6))