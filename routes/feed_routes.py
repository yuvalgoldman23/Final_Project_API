from flask import Blueprint, request, jsonify
from auth import auth_required
import datetime
import services.feed_services as service
feed_routes = Blueprint('feed_routes', __name__)


# A Post could include either mentions (of other users) or hashtags (of media content)
# Both mentions and hashtags are lists (we could mention multiple people or movies - or none) - would probably be smart to limit their sizes
# A post belongs to a certain user
# A post could have other posts linked above it and below it (a parent-child relationship) as comments to a post.
# We want to be able to display all posts of a certain user (token not required)
# We want to allow a user to only edit/remove posts by himself (token required)
# We want to allow getting all posts mentioning a certain content (no token required) - later, delivery with content page?
# Fields of a post in the server side: post_id, user_id (owner), parent_post_id, child_post_id, mentions_list, hashtags_list, creation_date


@feed_routes.route('/feed', methods=['POST'])
@auth_required
def add_post(token_info):
    user_id = token_info.get('sub')
    data = request.json
    text_content = data.get('text_content')
    if not text_content:
        return jsonify({'error': 'No text content provided'}), 400
    parent_id = data.get('parent_id', None)
    is_child = data.get('is_child')
    if not is_child:
        return jsonify({'error': 'No is_child provided'}), 400
    # TODO mentions and tags shall both be arrays filled with sub arrays of tag id, starting index and length
    mentions = data.get('mentions')
    tags = data.get('tags')
    # First create the post-entry in the DB, then later add the tags and mentions, once we have a post id
    db_response  = service.add_post(user_id, parent_id, is_child, text_content)
    if len(db_response) == 2:
        error, status = db_response
        return jsonify({'error': error}), status
    else:
        # Only a single response value - thus success
        post_id = db_response
        # Now add the tags and mentions into the DB, linked to the newly created post id
        mentions_id = []
        tags_id = []
        for mention in mentions:
            new_mention = service.add_mention(post_id, mention.get('mentioned_user_id'), mention.get('start_position'), mention.get('length'))
            if not new_mention:
                #  Remove post, since it wasn't fully created
                service.remove_post(post_id)
                return jsonify({'error': 'Error adding mention to post, please try sending request again'}), 400
            mentions_id.append((new_mention, mention.get('mentioned_user_id')))
        for tag in tags:
            new_tag = service.add_tag(post_id, tag.get('tagged_media_id'), tag.get('start_position'), tag.get('length'))
            if not new_tag:
                #  Remove post, since it wasn't fully created
                service.remove_post(post_id)
                return jsonify({'error': 'Error adding tag to post, please try sending request again'}), 400
            tags_id.append((new_tag, tag.get('tagged_media_id')))
        return jsonify({'post_id': post_id, 'mentions': mentions_id, 'tags': tags_id}), 200


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
