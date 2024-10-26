# routes/recommendation_routes.py

import copy
import math
import random
import utils

import numpy as np
import requests
import torch
import torch.nn as nn
import torch.nn.functional as F
from flask import Blueprint, request
import services.watchlist_services as ws
import routes.watchlist_routes as rt
from auth import auth_required
from database_connector import connection, cursor, cursor2

recommendation_routes = Blueprint('recommendation_routes', __name__)

query = f"SELECT * FROM media_data "
cursor2.execute(query)

movie_data = cursor2.fetchall()

query = f"SELECT media_ID, is_movie, AVG(rating) AS avg_rating, COUNT(User_ID) AS num_raters FROM rating GROUP BY media_ID, is_movie HAVING AVG(rating) >= 7; "
cursor2.execute(query)

recommendation_candidates = cursor2.fetchall()
api_key = '2e07ce71cc9f7b5a418b824c87bcb76f'

for r in recommendation_candidates:
    r['weight'] = math.sqrt(r['num_raters'])
total_weight = sum(r['weight'] for r in recommendation_candidates)
for r in recommendation_candidates:
    r['probability'] = r['weight'] / total_weight


def greedy_random_selection(Recomandation_canidentes):
    rand = random.random()  # Random float between 0 and 1
    cumulative_probability = 0.0
    for media in Recomandation_canidentes:
        cumulative_probability += media['probability']
        if rand <= cumulative_probability:
            return media


def create_genre_matrix(genres_str):
    genre_ids = [int(id) for id in genres_str.split(',') if id]
    # Number of rows and columns
    num_rows = 5
    num_cols = 19  # TMDb has 19 standard movie genres
    matrix = np.zeros((num_rows, num_cols), dtype=int)
    # Complete mapping of TMDb genre IDs to column indices
    genre_id_to_col = {
        28: 0,  # Action
        12: 1,  # Adventure
        16: 2,  # Animation
        35: 3,  # Comedy
        80: 4,  # Crime
        99: 5,  # Documentary
        18: 6,  # Drama
        10751: 7,  # Family
        14: 8,  # Fantasy
        36: 9,  # History
        27: 10,  # Horror
        10402: 11,  # Music
        9648: 12,  # Mystery
        10749: 13,  # Romance
        878: 14,  # Science Fiction
        10770: 15,  # TV Movie
        53: 16,  # Thriller
        10752: 17,  # War
        37: 18  # Western
    }
    limited_genre_ids = genre_ids[:num_rows]
    # Populate the matrix with one-hot encoding in each row
    for i, genre_id in enumerate(limited_genre_ids):
        col_index = genre_id_to_col.get(genre_id)
        if col_index is not None:
            matrix[i, col_index] = 1.0

    return matrix.astype(float)


# Define the neural network model
class DNNModel(nn.Module):
    def __init__(self):
        super(DNNModel, self).__init__()
        self.fc1 = nn.Linear(5 * 19, 128)  # Flatten 5x19 input to 95 features, then 128 neurons in the first layer
        self.fc2 = nn.Linear(128, 64)  # Second layer with 64 neurons
        self.fc3 = nn.Linear(64, 64)  # Third layer with 64 neurons
        self.fc4 = nn.Linear(64, 32)  # Fourth layer with 32 neurons
        self.fc5 = nn.Linear(32, 2)  # Output layer for 2 classes (class 1 and class 0)

    def forward(self, x):
        x = x.view(-1, 5 * 19)  # Flatten the matrix input
        x = F.leaky_relu(self.fc1(x), negative_slope=0.01)  # Leaky ReLU with negative slope 0.01
        x = F.leaky_relu(self.fc2(x), negative_slope=0.01)  # Leaky ReLU for second layer
        x = F.leaky_relu(self.fc3(x), negative_slope=0.01)  # Leaky ReLU for third layer
        x = F.leaky_relu(self.fc4(x), negative_slope=0.01)  # Leaky ReLU for fourth layer
        x = torch.softmax(self.fc5(x), dim=1)  # Softmax output for class probabilities
        # x = torch.log_softmax(self.fc3(x), dim=1)
        return x


# Instantiate the model, loss function, and optimizer
model = DNNModel()

model.load_state_dict(torch.load("trained_modelv1_66_correct.pth"))
#model.load_state_dict(torch.load("C:\\Users\\Yanovsky\\Documents\\GitHub\\Final_Project_API\\trained_modelv1_66_correct.pth"))
trained_model = model


def get_movie_gen_by_id(api_key, movie_id):
    # Base URL for TMDb API
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    # Parameters including the API key
    params = {
        'api_key': api_key
    }

    # Sending GET request to the API
    response = requests.get(url, params=params)

    # If the request was successful
    if response.status_code == 200:
        movie = response.json()
        gen_str = ""
        for g in movie["genres"]:
            gen = g['id']
            gen_str = gen_str + str(gen) + ","
        return gen_str

    else:
        return ""


def get_tv_gen_by_id(api_key, tv_id):
    # Base URL for TMDb API
    url = f"https://api.themoviedb.org/3/tv/{tv_id}"

    # Parameters including the API key
    params = {
        'api_key': api_key
    }

    # Sending GET request to the API
    response = requests.get(url, params=params)

    # If the request was successful
    if response.status_code == 200:
        tv = response.json()
        gen_str = ""
        for g in tv["genres"]:
            gen = g['id']
            if gen < 10000:
                gen_str = gen_str + str(gen) + ","
            else:
                if gen == 10759:
                    gen_str = gen_str + "28" + "," + "12" + ","
                elif gen == 10765:
                    gen_str = gen_str + "14" + "," + "878" + ","
                elif gen == 10766:
                    gen_str = gen_str + "18" + ","
                elif gen == 10768:
                    gen_str = gen_str + "10752" + ","
                elif gen == 10762:
                    en_str = gen_str + "10751" + ","
                elif gen == 10764 or gen == 10763:
                    t = 5
                else:
                    gen_str = gen_str + str(gen) + ","
        return gen_str
    else:
        return ""


def check_compatibility(usr_rating, cannidate):
    like = 0
    dislike = 0
    movie_entry = next((movie for movie in movie_data if movie['id'] == cannidate), None)
    matrix_cannidate = create_genre_matrix(movie_entry['genres'])
    if movie_entry:
        for rating in usr_rating:
            if cannidate != rating["media_ID"]:
                matrix_rating = create_genre_matrix(rating['genres'])
                mat = (matrix_cannidate - matrix_rating) * (matrix_cannidate - matrix_rating)
                mat_tensor = torch.tensor(mat, dtype=torch.float32)
                propabillity = trained_model(mat_tensor)
                p1 = propabillity[0, 0].item()
                p2 = propabillity[0, 1].item()
                if rating['rating'] >= 7:
                    like = like + p1
                    dislike = dislike + p2
                else:
                    like = like + p2
                    dislike = dislike + p1
    # print(like)
    # print(dislike)
    if like >= dislike:
        return 1
    else:
        return 0


def check_compatibility_v2(usr_preperense, cannidate):
    like = 0.0
    dislike = 0.0
    matrix_cannidate = create_genre_matrix(cannidate)
    for p in usr_preperense:
        matrix_p = create_genre_matrix(p['gnr_str'])
        mat = (matrix_cannidate - matrix_p) * (matrix_cannidate - matrix_p)
        mat_tensor = torch.tensor(mat, dtype=torch.float32)
        propabillity = trained_model(mat_tensor)
        p1 = propabillity[0, 0].item()
        p2 = propabillity[0, 1].item()
        if p['is_liked']:
            like = like + p1
            dislike = dislike + p2
        else:
            like = like + p2
            dislike = dislike + p1
    return like, dislike


def get_media_recomandation():
    usr_id = request.args.get("usr_id")
    query = f"SELECT *  from rating where rating.User_ID = %s "
    cursor2.execute(query, (usr_id,))
    rating_of_usr = cursor2.fetchall()
    for r in rating_of_usr:
        if r['is_movie'] == 0:
            gen_str = get_tv_gen_by_id(api_key, r['media_ID'])
            r['genres'] = gen_str
        elif r['is_movie'] == 1:
            gen_str = get_movie_gen_by_id(api_key, r['media_ID'])
            r['genres'] = gen_str

    query_get_id = f"SELECT COALESCE( (SELECT ID FROM watch_lists_names WHERE User_ID = %s AND Main = 2),0) AS Recomendetion_list_id;"
    cursor2.execute(query_get_id, (usr_id,))
    id = cursor2.fetchall()[0]["Recomendetion_list_id"]
    if id == 0 or id == "0":
        create_id_query = f"INSERT INTO watch_lists_names (User_ID, name, Main) VALUES ( %s, 'Recomendetion_list', 2);"
        cursor.execute(create_id_query, (usr_id,))
        connection.commit()
        query_get_id = f"SELECT COALESCE( (SELECT ID FROM watch_lists_names WHERE User_ID = %s AND Main = 2),0) AS Recomendetion_list_id;"
        cursor2.execute(query_get_id, (usr_id,))
        id = cursor2.fetchall()[0]["Recomendetion_list_id"]

    added_tolist = 0
    while 1:
        if added_tolist == 5:
            break
        randmovie = random.choice(movie_data)
        if not any(obj.get('media_ID') == randmovie["id"] for obj in rating_of_usr):
            is_good = check_compatibility(rating_of_usr, randmovie["id"])
            if is_good == 1 or is_good == "1":
                query_add_to_watch_list = f"INSERT INTO watch_lists_objects ( Parent_ID, TMDB_ID, User_ID, is_movie) VALUES (%s, %s, %s, %s);"
                cursor.execute(query_add_to_watch_list, (id, randmovie["id"], usr_id, randmovie["is_movie"]))
                connection.commit()
                added_tolist = added_tolist + 1
            # return str(is_good)

    return id
    # return  usr_id


def get_tv_show_info(tv_show_id):
    url = f"https://api.themoviedb.org/3/tv/{tv_show_id}"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()
    return data


def get_movie_info(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()
    return data


import requests


def get_movie_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos"
    params = {
        "api_key": api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
    except requests.exceptions.HTTPError:
        return None

    youtube_trailer = None
    results = data.get('results', [])
    for video in results:
        if video.get('site') == 'YouTube' and video.get('type') == 'Trailer':
            youtube_trailer = video.get('key')
            break

    return youtube_trailer


def get_tv_trailer(tv_id):
    url = f"https://api.themoviedb.org/3/tv/{tv_id}/videos"  # Changed to /tv/ endpoint
    params = {
        "api_key": api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
    except requests.exceptions.HTTPError:
        return None

    youtube_trailer = None
    results = data.get('results', [])
    for video in results:
        if video.get('site') == 'YouTube' and video.get('type') == 'Trailer':
            youtube_trailer = video.get('key')
            break

    return youtube_trailer


@recommendation_routes.route('/api/watchlists/recommendation2', methods=['GET'])
def get_recommendation2():
   try:
    data = request.json
    usr_id = data.get('user_id')

    check_query = """
                                 SELECT COALESCE(
                                     (SELECT ID 
                                      FROM watch_lists_names 
                                      WHERE User_ID = %s AND Main = 2), 0) AS watchlist_id;
                                 """
    cursor2.execute(check_query, (usr_id,))
    result = cursor2.fetchone()

    watchlist_id = result['watchlist_id']
    if watchlist_id == "0":
        return {"Content": [], "ID": "0"}, 200
    watchlist_object = ws.get_watchlist_by_id(watchlist_id)
    if utils.is_db_response_error(watchlist_object):
        return {'Error': str(watchlist_object)}, 404
    extracted_watchlist = [
        {
            'TMDB_ID': item.get('TMDB_ID'),
            'is_movie': item.get('is_movie'),
            'ID': item.get('ID')
        }
        for item in watchlist_object
        if item.get('TMDB_ID') is not None
    ]
    # Fetch movies asynchronously, passing both TMDB_ID and is_movie
    movie_data_list = rt.run_async(rt.fetch_movies, extracted_watchlist, api_key, usr_id, watchlist_id)

    # Filter out None values and construct the result
    result = [movie_data for movie_data in movie_data_list if movie_data is not None]

    # Return the result as a dictionary
    return {"Content": result, "ID": watchlist_id}, 200
   except requests.exceptions.HTTPError:

       return {"Error:": "error"}, 404

@recommendation_routes.route('/api/watchlists/recommendation', methods=['GET'])
@auth_required
def get_recommendation(token_info):
   try:
    #data = request.json
    #usr_id = data.get('user_id')
    usr_id=token_info.get('sub')

    check_query = """
                                 SELECT COALESCE(
                                     (SELECT ID 
                                      FROM watch_lists_names 
                                      WHERE User_ID = %s AND Main = 2), 0) AS watchlist_id;
                                 """
    cursor2.execute(check_query, (usr_id,))
    result = cursor2.fetchone()

    watchlist_id = result['watchlist_id']
    if watchlist_id == "0":
        return {"Content": [], "ID": "0"}, 200
    watchlist_object = ws.get_watchlist_by_id(watchlist_id)
    if utils.is_db_response_error(watchlist_object):
        return {'Error': str(watchlist_object)}, 404
    extracted_watchlist = [
        {
            'TMDB_ID': item.get('TMDB_ID'),
            'is_movie': item.get('is_movie'),
            'ID': item.get('ID')
        }
        for item in watchlist_object
        if item.get('TMDB_ID') is not None
    ]
    # Fetch movies asynchronously, passing both TMDB_ID and is_movie
    movie_data_list = rt.run_async(rt.fetch_movies, extracted_watchlist, api_key, usr_id, watchlist_id)

    # Filter out None values and construct the result
    result = [movie_data for movie_data in movie_data_list if movie_data is not None]

    # Return the result as a dictionary
    return {"Content": result, "ID": watchlist_id}, 200
   except requests.exceptions.HTTPError:

       return {"Error:": "error"}, 404


@recommendation_routes.route('/api/recommendation_feedbackv2', methods=['GET'])
def update_prefrences2():
   try:
    data = request.json
    usr_id = data.get('user_id')
    is_movie= data.get('is_movie')
    media_id= data.get('media_id')
    liked = data.get("is_liked")
    algorithm = data.get("algorithm")
    query = f"SELECT COALESCE(  (SELECT ID  FROM recommendation_info  WHERE media_id = %s AND is_movie = %s AND user_ID = %s), '0') AS feedback_id;"
    cursor2.execute(query, (media_id, is_movie, usr_id))
    feedback_id = cursor2.fetchall()
    check_query = """
                             SELECT COALESCE(
                                 (SELECT ID 
                                  FROM watch_lists_names 
                                  WHERE User_ID = %s AND Main = 2), 0) AS watchlist_id;
                             """
    cursor2.execute(check_query, (usr_id,))
    result = cursor2.fetchone()

    watchlist_id = result['watchlist_id']

    if  feedback_id[0]["feedback_id"] == '0':
        insert_query = "  INSERT INTO recommendation_info (media_id, is_movie, user_ID, liked, Algorithm)  VALUES (%s, %s, %s, %s, %s)   "
        cursor.execute(insert_query, (media_id, is_movie, usr_id, liked, algorithm))
        if liked == 1 or liked == "1":


            # If no such watchlist exists (watchlist_id is 0), insert a new one
            if  watchlist_id[0] == '0':

                insert_query = """
                             INSERT INTO watch_lists_names ( User_ID, name, Main)
                             VALUES ( %s, "Recommendation",2)                        
                             """
                cursor.execute(insert_query, (usr_id,))
                connection.commit()
            check_query = """
                                      SELECT COALESCE(
                                          (SELECT ID 
                                           FROM watch_lists_names 
                                           WHERE User_ID = %s AND Main = 2), 0) AS watchlist_id;
                                      """
            cursor2.execute(check_query, (usr_id,))
            result = cursor2.fetchone()

            watchlist_id = result['watchlist_id']
            insert_query = """
                         INSERT INTO watch_lists_objects ( Parent_ID, TMDB_ID, user_ID, is_movie)
                         VALUES ( %s, %s, %s, %s);
                         """
            cursor.execute(insert_query, (watchlist_id, media_id, usr_id, int(is_movie)))

    else:

        update_query = "  UPDATE recommendation_info  SET liked = %s, Algorithm = %s  WHERE ID = %s  "
        cursor.execute(update_query, (liked, algorithm, feedback_id[0]["feedback_id"]))
    connection.commit()
    watchlist_object = ws.get_watchlist_by_id(watchlist_id)
    if utils.is_db_response_error(watchlist_object):
        return {'Error': str(watchlist_object)}, 404

    # Extract TMDB IDs and is_movie from the watchlist object
    extracted_watchlist = [
        {
            'TMDB_ID': item.get('TMDB_ID'),
            'is_movie': item.get('is_movie'),
            'ID': item.get('ID')
        }
        for item in watchlist_object
        if item.get('TMDB_ID') is not None
    ]

    if watchlist_id == "0":
        return {"Content": [], "ID": "0"}, 200
    api_key = '2e07ce71cc9f7b5a418b824c87bcb76f'

    # Fetch movies asynchronously, passing both TMDB_ID and is_movie
    movie_data_list = rt.run_async(rt.fetch_movies, extracted_watchlist, api_key, usr_id, watchlist_id)

    # Filter out None values and construct the result
    result = [movie_data for movie_data in movie_data_list if movie_data is not None]

    # Return the result as a dictionary
    return {"Content": result, "ID": watchlist_id}, 200


   except requests.exceptions.HTTPError:

       return {"Error:": "error"}, 404


@recommendation_routes.route('/api/recommendation_feedback', methods=['POST'])
@auth_required
def update_preferences(token_info):
 try:
    data = request.json
    usr_id = token_info.get('sub')
    is_movie = data.get('is_movie')
    media_id = data.get('media_id')
    liked = data.get("is_liked")
    algorithm = data.get("algorithm")
    query = f"SELECT COALESCE(  (SELECT ID  FROM recommendation_info  WHERE media_id = %s AND is_movie = %s AND user_ID = %s), '0') AS feedback_id;"
    cursor2.execute(query, (media_id, is_movie, usr_id))
    feedback_id = cursor2.fetchall()
    check_query = """
                                 SELECT COALESCE(
                                     (SELECT ID 
                                      FROM watch_lists_names 
                                      WHERE User_ID = %s AND Main = 2), 0) AS watchlist_id;
                                 """
    cursor2.execute(check_query, (usr_id,))
    result = cursor2.fetchone()

    watchlist_id = result['watchlist_id']

    if feedback_id[0]["feedback_id"] == '0':
        insert_query = "  INSERT INTO recommendation_info (media_id, is_movie, user_ID, liked, Algorithm)  VALUES (%s, %s, %s, %s, %s)   "
        cursor.execute(insert_query, (media_id, is_movie, usr_id, liked, algorithm))
        if liked == 1 or liked == "1":

            # If no such watchlist exists (watchlist_id is 0), insert a new one
            if watchlist_id[0] == '0':
                insert_query = """
                                 INSERT INTO watch_lists_names ( User_ID, name, Main)
                                 VALUES ( %s, "Recommendation",2)                        
                                 """
                cursor.execute(insert_query, (usr_id,))
                connection.commit()
            check_query = """
                                          SELECT COALESCE(
                                              (SELECT ID 
                                               FROM watch_lists_names 
                                               WHERE User_ID = %s AND Main = 2), 0) AS watchlist_id;
                                          """
            cursor2.execute(check_query, (usr_id,))
            result = cursor2.fetchone()

            watchlist_id = result['watchlist_id']
            insert_query = """
                             INSERT INTO watch_lists_objects ( Parent_ID, TMDB_ID, user_ID, is_movie)
                             VALUES ( %s, %s, %s, %s);
                             """
            cursor.execute(insert_query, (watchlist_id, media_id, usr_id, int(is_movie)))

    else:

        update_query = "  UPDATE recommendation_info  SET liked = %s, Algorithm = %s  WHERE ID = %s  "
        cursor.execute(update_query, (liked, algorithm, feedback_id[0]["feedback_id"]))
    connection.commit()
    if watchlist_id == "0":
        return {"Content": [], "ID": "0"}, 200
    watchlist_object = ws.get_watchlist_by_id(watchlist_id)
    if utils.is_db_response_error(watchlist_object):
        return {'Error': str(watchlist_object)}, 404

    # Extract TMDB IDs and is_movie from the watchlist object
    extracted_watchlist = [
        {
            'TMDB_ID': item.get('TMDB_ID'),
            'is_movie': item.get('is_movie'),
            'ID': item.get('ID')
        }
        for item in watchlist_object
        if item.get('TMDB_ID') is not None
    ]

    api_key = '2e07ce71cc9f7b5a418b824c87bcb76f'

    # Fetch movies asynchronously, passing both TMDB_ID and is_movie
    movie_data_list = rt.run_async(rt.fetch_movies, extracted_watchlist, api_key, usr_id, watchlist_id)

    # Filter out None values and construct the result
    result = [movie_data for movie_data in movie_data_list if movie_data is not None]

    # Return the result as a dictionary
    return {"Content": result, "ID": watchlist_id}, 200

 except requests.exceptions.HTTPError:

  return "0"


def filter_fields(data, fields):
    """
    Filters the input data to return only the specified fields.

    Parameters:
    data (dict): The dictionary containing the data.
    fields (list): A list of field names that need to be included in the output.

    Returns:
    dict: A new dictionary with only the specified fields.
    """
    return {key: data[key] for key in fields if key in data}


@recommendation_routes.route('/api/Media_recommendation', methods=['GET'])
@auth_required
def get_media_recommendationv2(token_info):
    print("starting recommendation process")
    fields_to_keep = ["title", "release_date", "vote_average", "Recommended_by", "trailer", "poster_path",
                      "overview", "name", "Is_movie", "genres"]
    usr_id = token_info.get('sub')
    query = f"SELECT *  from rating where rating.User_ID = %s "
    cursor2.execute(query, (usr_id,))
    rating_of_usr = cursor2.fetchall()
    usr_prefrence = []
    for r in rating_of_usr:
        if r['is_movie'] == 0:
            gen_str = get_tv_gen_by_id(api_key, r['media_ID'])
            r['genres'] = gen_str
        elif r['is_movie'] == 1:
            gen_str = get_movie_gen_by_id(api_key, r['media_ID'])
            r['genres'] = gen_str
        p = {}
        p["media_Id"] = r["media_ID"]
        p['gnr_str'] = r['genres']
        p['is_movie'] = r['is_movie']
        if r['rating'] >= 7:
            p['is_liked'] = 1
        else:
            p['is_liked'] = 0
        usr_prefrence.append(p)
    # return usr_prefrence
    algo_recommendation = []
    while 1:
        if len(algo_recommendation) == 5:
            break
        can = greedy_random_selection(recommendation_candidates)
        can_gnr_str = ""
        if (can["is_movie"]):
            can_gnr_str = get_movie_gen_by_id(api_key, can["media_ID"])
        else:
            can_gnr_str = get_tv_gen_by_id(api_key, can["media_ID"])
        can_like, can_dislike = check_compatibility_v2(usr_prefrence, can_gnr_str)
        if (can_like > can_dislike):
            can_copy = copy.deepcopy(can)
            can_copy["likelihood"] = can_like - can_dislike
            algo_recommendation.append(can_copy)
    return_arr = []
    print("after while, with recs of", algo_recommendation)
    for a in algo_recommendation:

        if a["is_movie"]:
            info = get_movie_info(a["media_ID"])
            t = get_movie_trailer(a["media_ID"])
            info["trailer"] = t
            info["recommended_by"] = "Algorithm1"
            info["is_movie"] = 1
            info["tmdb_id"]= a["media_ID"]
            info = filter_fields(info, fields_to_keep)
            info["streaming_services"] = None
            info["user_id"] = "0"
            info["user_rating"] = 0
            info["video_links"] = []
            info["item_id"] = "0"
            info["list_id"] = None
            info["tmdb_rating"] = 1.0
            # TODO missing the default path, doesn't protect against no image....
            info["small_poster_path"] = "https://image.tmdb.org/t/p/w200/" + info[
                "poster_path"]
            info["poster_path"] = "https://image.tmdb.org/t/p/original/" + info[
                "poster_path"]
        else:
            info = get_tv_show_info(a["media_ID"])
            t = get_tv_trailer(a["media_ID"])
            info["trailer"] = t
            info["Recommended_by"] = "Algorithm1"
            info["Is_movie"] = 0

            info = filter_fields(info, fields_to_keep)
            info["streaming_services"] = None
            info["user_id"] = "0"
            info["user_rating"] = 0
            info["video_links"] = []
            info["item_id"] = "0"
            info["list_id"] = None
            info["tmdb_rating"] = 1.0
            info["small_poster_path"] = "https://image.tmdb.org/t/p/w200/" + info[
                "poster_path"]
            info["poster_path"] = "https://image.tmdb.org/t/p/original/" + info[
                "poster_path"]
        return_arr.append(info)

    return return_arr