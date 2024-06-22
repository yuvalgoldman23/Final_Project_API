from flask import Blueprint, request, jsonify
from auth import auth_required
import services.reviews_services as service

reviews_routes = Blueprint('reviews_routes', __name__)


@reviews_routes.route('/api/reviews', methods=['POST'])
@auth_required
def write_review(token_info):
    user_id = token_info.get('sub')
    data = request.json
    text = data.get('text')
    content_id = data.get('content_id')
    # TODO add is_movie since we could have conflicting ids that could be both?
    if not text or not content_id:
        return jsonify({'status': 'error', 'message': 'Missing text or content_id'}), 400
    else:
        return_val, status = service.write_review(user_id, content_id, text)[0]
        if status != 201:
            return jsonify({'status': 'error', 'message': return_val}), status
        return jsonify({'success': f'added a review for {content_id}', 'review_id' : return_val}), 201

@reviews_routes.route('/api/users/reviews', methods=['GET'])
def get_reviews_by_user():
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'status': 'error', 'message': 'Missing user_id'}), 400
    else:
        return_val, status = service.get_reviews_by_user(user_id)
        if status != 200:
            return jsonify({'status': 'error', 'message': return_val}), status
        return jsonify({'reviews': return_val}), 200


@reviews_routes.route('/api/reviews/content', methods=['GET'])
def get_reviews_by_content():
    data = request.json
    content_id = data.get('content_id')
    if not content_id:
        return jsonify({'status': 'error', 'message': 'Missing content_id'}), 400
    else:
        return_val, status = service.get_reviews_by_content(content_id)
        print(return_val)
        if status != 200:
            return jsonify({'status': 'error', 'message': return_val}), status
        return jsonify({'reviews': return_val}), 200

@reviews_routes.route('/api/reviews', methods=['DELETE'])
@auth_required
def delete_reviews(token_info):
    user_id = token_info.get('sub')
    data = request.json
    review_id = data.get('review_id')
    if not review_id:
        return jsonify({'status': 'error', 'message': 'Missing review_id'}), 400
    else:
        return_val, status = service.Remove_Review(review_id, user_id)
        if status != 200:
            return jsonify({'status': 'error', 'message': return_val}), status
        else:
            return jsonify({'success': f'deleted review of id {review_id}'}), 200