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
        return jsonify({'status': return_val}), status


@ratings_routes.route('/api/users/ratings', methods=['GET'])
@auth_required
def get_ratings_by_user(token_info):
    # If no user_id received in data,return ratings for logged in user
    try:
        data = request.json
        user_id = data.get('user_id')
    except:
        user_id = token_info.get('sub')
    db_response, status = service.get_rating_of_user(user_id)
    if status != 200:
        return jsonify({'status' : db_response}), status
    else:
        print("db response" , db_response)
        return jsonify({'ratings': db_response}), 200



@ratings_routes.route('/api/ratings', methods = ['DELETE'])
@auth_required
def remove_review(token_info):
    data = request.json
    rating_object_id = data.get('rating_object_id')
    user_id = token_info.get('sub')
    if not rating_object_id:
        return jsonify({'status': "Must provide content id to be deleted"}), 404
    else:
        db_response, status = service.Remove_rating(rating_object_id, user_id)
        return jsonify({'status': db_response}), status