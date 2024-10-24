import asyncio

import aiohttp
from flask import Blueprint, request, jsonify, json

import utils
from auth import auth_required
import services.rating_services as service
import routes.tmdb_routes as tmdb
from List import ListItem, List

class RatingList(List):
    def __init__(self, user_id):
        # As of now, our ratings list doesn't have a list_id - it's one of a kind
        super().__init__(user_id, None)
    def populate_raw_objects(self):
        # Use 'get user ratings' to get all the raw rating objects
        # Call the service to get all ratings by the logged in user
        db_response, status = service.get_rating_of_user(self.user_id, None, None)
        # Return the appropriate response based on the status
        if status != 200:
            # TODO Think about how to handle an error here, since the init handles this function and the next one
            print("there was an error populating the ratings list raw objects")
            return db_response, status
        else:
            self.raw_objects = db_response
            for raw_object in self.raw_objects:
                new_item = ListItem(raw_object['is_movie'], raw_object['media_ID'], raw_object['User_ID'],
                                    raw_object['ID'], self.list_id)
                self.content.append(new_item)
            return "success", 200
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
        if status != 201 and status != 200:
            return jsonify({'db_response': return_val}), status
        else:
            return jsonify({'rating_id': return_val, 'new_ratings': get_ratings_list_data(user_id)}), status

@ratings_routes.route('/api/users/ratings_list', methods=['GET'])
@auth_required
def get_user_ratings_list(token_info):
    print("got api request for ratings_list")
    user_id = token_info.get('sub')
    # Get the ratings list for the currently logged in user
    # TODO think about handling errors here....
    ratings_list = RatingList(user_id)
    return jsonify(ratings_list.to_dict()), 200



@ratings_routes.route('/api/users/ratings', methods=['GET'])
@auth_required
def old_get_ratings_by_user(token_info):
    # Safely parse JSON data from the request
    data = request.get_json(silent=True)
    # Determine user_id: from request if present, otherwise from token_info
    if data and 'user_id' in data:
        user_id = data['user_id']
    else:
        user_id = token_info.get('sub')

    # Determine content_id and is_movie: from request if present, otherwise None
    if data and 'content_id' in data:
        if 'is_movie' in data:
            content_id = data['content_id']
            is_movie = data['is_movie']
        else:
            return jsonify({'error': 'Content ID and is_movie must be provided together'}), 400
    else:
        content_id = None
        is_movie = None

    # Call the service to get ratings
    db_response, status = service.get_rating_of_user(user_id, content_id, is_movie)
    # Return the appropriate response based on the status
    if status != 200:
        return jsonify({'db_response': db_response}), status
    else:
        #print("db response", db_response)
        return jsonify({'ratings': db_response}), 200


@ratings_routes.route('/api/ratings', methods = ['PUT','DELETE'])
@auth_required
def remove_update_rating(token_info):
    data = request.json
    print("delete rating request content", data)
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
    print("new ratings are", get_ratings_list_data(user_id))
    return jsonify({'db_response': db_response, 'new_ratings': get_ratings_list_data(user_id)}), status



# Async ratings list endpoint
# TODO change the endpoint naming eventually


async def fetch_movie(session, content_id, is_movie, api_key, item_id, rating, user_id):
    movie_url = f"https://api.themoviedb.org/3/movie/{content_id}?api_key={api_key}&append_to_response=videos"
    tv_url = f"https://api.themoviedb.org/3/tv/{content_id}?api_key={api_key}&append_to_response=videos"

    async with session.get(movie_url if is_movie else tv_url) as response:
        if response.status == 200:
            data = await response.json()

            # Initialize media_info
            media_info = {}

            # Constructing the media_info object based on whether it's a movie or a series
            media_info['title'] = data.get('original_title') if is_movie else data.get('original_name')
            media_info['genres'] = [genre['name'] for genre in data.get('genres', [])]
            media_info['tmdb_id'] = content_id
            media_info['is_movie'] = is_movie

            # Poster paths
            poster_path = data.get('poster_path')
            if poster_path:
                media_info['poster_path'] = f"https://image.tmdb.org/t/p/original/{poster_path}"
                media_info['small_poster_path'] = f"https://image.tmdb.org/t/p/w200/{poster_path}"
            else:
                media_info['poster_path'] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
                media_info['small_poster_path'] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"

            # Overview
            media_info['overview'] = data.get('overview')

            # Release date
            media_info['release_date'] = data.get('release_date') if is_movie else data.get('first_air_date')

            # TMDB rating
            media_info['tmdb_rating'] = data.get('vote_average')

            # Video links
            videos = data.get('videos', {}).get('results', [])
            media_info['video_links'] = videos[0].get('key') if videos else None

            # Additional info
            media_info['list_item_id'] = item_id
            media_info['user_rating'] = rating
            media_info['user_id'] = user_id

            return media_info
        else:
            return None  # Handle errors appropriately


async def fetch_movies(content_info, api_key, user_id):
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(fetch_movie(session, item['TMDB_ID'], item['is_movie'], api_key, item['ID'], item['user_rating'], user_id))
            for item in content_info
        ]
        return await asyncio.gather(*tasks)


def run_async(func, *args):
    return asyncio.run(func(*args))


def get_ratings_list_data(user_id):
    """
    This helper function handles fetching the user's ratings and movie data.
    It returns the result as a Python dictionary, ready to be used internally or by the endpoint.
    """
    rating_list_object, status = service.get_rating_of_user(user_id, None, None)
    if utils.is_db_response_error(rating_list_object) or status != 200:
        return {'Error': str(rating_list_object)}, 404

    # Extract TMDB IDs, is_movie, and user_rating from the rating list object
    extracted_ratings_list = [
        {
            'TMDB_ID': item.get('media_ID'),
            'is_movie': item.get('is_movie'),
            'ID': item.get('ID'),
            'user_rating': item.get('rating')
        }
        for item in rating_list_object
        if item.get('media_ID') is not None
    ]

    api_key = '2e07ce71cc9f7b5a418b824c87bcb76f'

    # Fetch movies asynchronously, passing both TMDB_ID and is_movie
    movie_data_list = run_async(fetch_movies, extracted_ratings_list, api_key, user_id)

    # Filter out None values and construct the result
    result = [movie_data for movie_data in movie_data_list if movie_data is not None]

    # Return the result as a dictionary
    return {"Content": result}, 200


@ratings_routes.route('/api/ratings/async', methods=['GET'])
@auth_required
def async_get_ratings_list(token_info):
    """
    Endpoint for fetching the user's ratings list. It uses the helper function
    and returns the result as a JSON response.
    """
    user_id = token_info.get('sub')

    # Call the helper function and get the result
    result, status_code = get_ratings_list_data(user_id)

    # Return the result using jsonify for the API response
    return jsonify(result), status_code

