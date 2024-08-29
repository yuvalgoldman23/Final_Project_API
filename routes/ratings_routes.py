from flask import Blueprint, request, jsonify, json

import utils
from auth import auth_required
import services.rating_services as service
import routes.tmdb_routes as tmdb
ratings_routes = Blueprint('ratings_routes', __name__)

@ratings_routes.route('/api/ratings', methods=['POST'])
@auth_required
def add_rating(token_info):
    data = request.json
    user_id = token_info.get('sub')
    content_id = data.get('content_id')
    rating = data.get('rating')
    is_movie = data.get('is_movie')
    print("is_movie", is_movie)
    if not content_id or not content_id or is_movie is None:
        return jsonify({'error': 'Content ID and Rating must be provided'}), 400
    else:
        return_val, status = service.Add_rating(user_id, content_id, rating, is_movie)
        if status != 201:
            return jsonify({'error': return_val}), status
        else:
            return jsonify({'rating_id': return_val}), status


@ratings_routes.route('/api/users/ratings', methods=['GET'])
@auth_required
def get_ratings_by_user(token_info):
    # If no user_id received in data,return ratings for logged in user
    if request.json and request.json.get('user_id'):
        user_id = request.json.get('user_id')
    else:
        user_id = token_info.get('sub')
    if request.json and request.json.get('content_id') and request.json.get('is_movie'):
        content_id = request.json.get('content_id')
        is_movie = request.json.get('is_movie')
    else:
        content_id = None
        is_movie = None
    db_response, status = service.get_rating_of_user(user_id, content_id, is_movie)
    if status != 200:
        return jsonify({'status' : db_response}), status
    else:
        print("db response" , db_response)
        return jsonify({'ratings': db_response}), 200



@ratings_routes.route('/api/ratings', methods = ['PUT','DELETE'])
@auth_required
def remove_update_rating(token_info):
    data = request.json
    content_id = data.get('content_id')
    is_movie = data.get('is_movie')
    user_id = token_info.get('sub')
    if not content_id or is_movie is None:
        return jsonify({'status': "Must provide content id and is_movie fields to be deleted/updated"}), 404
    if not data.get("new_rating"):
        db_response, status = service.Remove_rating(content_id,is_movie, user_id)
    else:
        new_rating = data.get('new_rating')
        db_response, status = service.update_rating(content_id,is_movie, user_id, new_rating)
    return jsonify({'status': db_response}), status