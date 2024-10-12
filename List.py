from flask import request, jsonify
from auth import auth_required
from routes.tmdb_routes import get_movie_info, get_tv_show_info
import services.rating_services as rating_service


class ListItem:
    def __init__(self, is_movie, tmdb_id, user_id, item_id, list_id):
        self.is_movie = is_movie
        self.tmdb_id = tmdb_id
        self.user_id = user_id
        self.title = None
        self.genres = None
        self.poster_path = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
        self.small_poster_path = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
        self.overview = None
        self.release_date = None
        self.tmdb_rating = None
        self.user_rating = None
        self.video_links = None
        self.streaming_services = None
        # TODO do we need to have similar films for every list item?
        self.similar_movies = None
        self.item_id = item_id
        self.list_id = list_id
        self.process_data()

    def process_data(self):
        if self.is_movie:
            tmdb_info = get_movie_info(self.tmdb_id)
        else:
            tmdb_info = get_tv_show_info(self.tmdb_id)
        if self.is_movie:
            tmdb_info = jsonify(tmdb_info)
        tmdb_info = tmdb_info.json
        self.title = tmdb_info['title'] if self.is_movie else tmdb_info['name']
        self.genres = [genre['name'] for genre in tmdb_info['genres']]
        if tmdb_info['poster_path']:
            self.poster_path = "https://image.tmdb.org/t/p/original/" + tmdb_info['poster_path']
            self.small_poster_path = "https://image.tmdb.org/t/p/w200/" + tmdb_info['poster_path']

        self.overview = tmdb_info.get('overview')
        self.release_date = tmdb_info.get('release_date') if self.is_movie else tmdb_info.get('first_air_date')
        self.tmdb_rating = tmdb_info.get('vote_average')
        if "videos" in tmdb_info and len(tmdb_info['videos']['results']) > 0:
            #print("the video selected is", tmdb_info.get('videos')['results'][0]['key'])
            self.video_links = [tmdb_info['videos']['results'][0]['key']]

        user_rating, status_code = rating_service.get_rating_of_user(self.user_id, self.tmdb_id, self.is_movie)
        if status_code == 200:
            self.user_rating = user_rating.get('rating')

    def to_dict(self):
        return {
            'is_movie': self.is_movie,
            'tmdb_id': self.tmdb_id,
            'user_id': self.user_id,
            'title': self.title,
            'genres': self.genres,
            'poster_path': self.poster_path,
            'small_poster_path': self.small_poster_path,
            'overview': self.overview,
            'release_date': self.release_date,
            'tmdb_rating': self.tmdb_rating,
            'user_rating': self.user_rating,
            'video_links': self.video_links,
            'streaming_services': self.streaming_services,
            'item_id': self.item_id,
            'list_id': self.list_id
        }

# A generic list class, to be inherited by watchlist and rating list classes
class List:
    def __init__(self, user_id, list_id):
        self.user_id = user_id
        self.list_id = list_id
        self.raw_objects = None
        self.content = []
        self.populate_raw_objects()
    # Add the raw list items into the list object, before further processing
    @auth_required
    def populate_raw_objects(self):
    # Contact the DB and ask for every item belonging to the current list
        pass
    def populate_content(self):
        for raw_object in self.raw_objects:
            # Create a new item with full details by using the raw details we initially have
            new_item = ListItem(raw_object['is_movie'], raw_object['tmdb_id'], raw_object['user_id'], raw_object['item_id'], self.list_id)
            self.content.append(new_item)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'list_id': self.list_id,
            'content': [item.to_dict() for item in self.content]
        }
