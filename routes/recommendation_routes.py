# routes/recommendation_routes.py

import copy
import math
import random
import utils
from collections import Counter
import numpy as np
import requests
import torch
import torch.nn as nn
import torch.nn.functional as F
from flask import Blueprint, request , session
import services.watchlist_services as ws
import routes.watchlist_routes as rt
from auth import auth_required
#from database_connector import connection, cursor, cursor2 ,connection_pool , semaphore
from database_connector import connection_pool , semaphore
from mysql.connector import Error
import time
import spacy
from itertools import combinations
from sentence_transformers import SentenceTransformer, util
from routes.streaming_providers_routes import media_page_streaming_services

nlp = spacy.load("en_core_web_md")
recommendation_routes = Blueprint('recommendation_routes', __name__)

def help():
 try:
  global  movie_data,  recommendation_candidates
  connection2 = connection_pool.get_connection()
  with connection2.cursor(dictionary=True) as cursor2:
   query = f"SELECT * FROM media_data "
   cursor2.execute(query)
   movie_data = cursor2.fetchall()
   query = f"SELECT media_ID, is_movie, AVG(rating) AS avg_rating, COUNT(User_ID) AS num_raters FROM rating GROUP BY media_ID, is_movie HAVING AVG(rating) >= 7; "
   cursor2.execute(query)
   recommendation_candidates = cursor2.fetchall()
 except mysql.connector.Error as err:
     t=5
 finally:
    if 'connection2' in locals() and connection2.is_connected():
        connection2.close()
help()
#recommendation_candidates = cursor2.fetchall()
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

#model.load_state_dict(torch.load("trained_modelv1_66_correct.pth"))
model.load_state_dict(torch.load("C:\\Users\\Yanovsky\\Documents\\GitHub\\Final_Project_API\\trained_modelv1_66_correct.pth"))
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

def get_tv_keywords(apikey,tv_id):
    url = f"https://api.themoviedb.org/3/tv/{tv_id}/keywords"

    # Parameters including the API key
    params = {
        'api_key': api_key
    }
    response = requests.get(url, params=params)

    # If the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return ""
def get_movie_keywords(apikey,movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/keywords"

    # Parameters including the API key
    params = {
        'api_key': api_key
    }
    response = requests.get(url, params=params)

    # If the request was successful
    if response.status_code == 200:
        return response.json()
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

model = SentenceTransformer('all-MiniLM-L6-v2')
def calculate_keyword_similarity(keywords):
    """
    Calculate semantic similarity between each pair of keywords in the input array.

    Parameters:
        keywords (list): A list of dictionaries, each containing 'count', 'id', and 'name' of a keyword.

    Returns:
        list: A list of dictionaries containing pairs of keywords and their similarity score.
    """
    similarities = []
    for (kw1, kw2) in combinations(keywords, 2):

        doc1 = nlp(kw1['name'])
        doc2 = nlp(kw2['name'])
        similarity = doc1.similarity(doc2)

        '''
        embedding1 = model.encode(kw1['name'])
        embedding2 = model.encode(kw2['name'])
        similarity = util.cos_sim(embedding1, embedding2)
        '''
        if similarity >=0.80:
         similarities.append({
            "keyword1": kw1['name'],
            "keyword2": kw2['name'],
            "id1": kw1["id"],
            "id2":kw2["id"],
            "count1":kw1["count"],
            "count2": kw2["count"],
            "similarity": similarity
         })

    # Sort by similarity in descending order
    similarities = sorted(similarities, key=lambda x: x['similarity'], reverse=True)

    return similarities

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

def get_movies_by_keyword(keyword_id):
    """Fetch movies associated with the keyword ID."""
    url = f"https://api.themoviedb.org/3/keyword/{keyword_id}/movies"
    params = {
        "api_key": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
     return response.json().get('results', [])
    else:
        return []

def get_tv_shows_by_keyword(keyword_id):
    """Fetch TV shows associated with the keyword ID."""
    url = f"https://api.themoviedb.org/3/discover/tv"
    params = {
        "api_key": api_key,
        "with_keywords": keyword_id
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
     return response.json().get('results', [])
    else:
        return []

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
    connection2 = connection_pool.get_connection()


    cursor4 = connection2.cursor(dictionary=True)
    cursor4.execute(check_query, (usr_id,))

    result = cursor4.fetchone()

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
   finally:
       if 'cursor3' in locals() and cursor3:
           cursor3.close()
       if 'cursor4' in locals() and cursor4:
           cursor4.close()
       if 'connection2' in locals() and not (connection2 is None):
           if connection2 and connection2.is_connected():
               connection2.close()


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

# Function to get the total count of movies for the keyword
def get_movie_count(api_key, keyword_id):
    url = f'https://api.themoviedb.org/3/keyword/{keyword_id}/movies'
    params = {'api_key': api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['total_results']  # This gives the count of movies
    else:
        print("Failed to retrieve data for movies:", response.json())
        return 0

# Function to get the total count of TV shows for the keyword
def get_tv_count(api_key, keyword_id):
    url = f'https://api.themoviedb.org/3/keyword/{keyword_id}/tv'
    params = {'api_key': api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['total_results']  # This gives the count of TV shows
    else:
        print("Failed to retrieve data for TV shows:", response.json())
        return 0


@recommendation_routes.route('/api/recommendation_feedback', methods=['POST'])
@auth_required
def update_preferences(token_info):
 semaphore.acquire()
 try:

    data = request.json
    usr_id = token_info.get('sub')
    is_movie = data.get('is_movie')
    media_id = data.get('media_id')
    liked = data.get("is_liked")
    algorithm = data.get("algorithm")
    connection2 = connection_pool.get_connection()

    cursor3 = connection2.cursor()
    cursor4 = connection2.cursor(dictionary=True)

    query = f"SELECT COALESCE(  (SELECT ID  FROM recommendation_info  WHERE media_id = %s AND is_movie = %s AND user_ID = %s), '0') AS feedback_id;"
    cursor4.execute(query, (media_id, is_movie, usr_id))
    feedback_id = cursor4.fetchall()
    check_query = """
                                 SELECT COALESCE(
                                     (SELECT ID 
                                      FROM watch_lists_names 
                                      WHERE User_ID = %s AND Main = 1), 0) AS watchlist_id;
                                 """
    cursor4.execute(check_query, (usr_id,))
    result = cursor4.fetchone()

    watchlist_id = result['watchlist_id']

    if feedback_id[0]["feedback_id"] == '0':
        insert_query = "  INSERT INTO recommendation_info (media_id, is_movie, user_ID, liked, Algorithm)  VALUES (%s, %s, %s, %s, %s)   "
        cursor3.execute(insert_query, (media_id, is_movie, usr_id, liked, algorithm))
        if liked == 1 or liked == "1":

            # If no such watchlist exists (watchlist_id is 0), insert a new one
            if watchlist_id == '0':
                insert_query = """
                                 INSERT INTO watch_lists_names ( User_ID, name, Main)
                                 VALUES ( %s, "Recommendation",2)                        
                                 """
                cursor3.execute(insert_query, (usr_id,))
                connection2.commit()
            check_query = """
                                          SELECT COALESCE(
                                              (SELECT ID 
                                               FROM watch_lists_names 
                                               WHERE User_ID = %s AND Main = 1), 0) AS watchlist_id;
                                          """
            cursor4.execute(check_query, (usr_id,))
            result = cursor4.fetchone()

            watchlist_id = result['watchlist_id']
            insert_query = """
                             INSERT INTO watch_lists_objects ( Parent_ID, TMDB_ID, user_ID, is_movie)
                             VALUES ( %s, %s, %s, %s);
                             """
            cursor3.execute(insert_query, (watchlist_id, media_id, usr_id, int(is_movie)))

    else:

        update_query = "  UPDATE recommendation_info  SET liked = %s, Algorithm = %s  WHERE ID = %s  "
        cursor3.execute(update_query, (liked, algorithm, feedback_id[0]["feedback_id"]))
    connection2.commit()
    print("Entered to feed back")
    '''
    if 'cursor3' in locals() and cursor3:
        cursor3.close()
    if 'cursor4' in locals() and cursor4:
        cursor4.close()
    if 'connection2' in locals() and not (connection2 is None):
        if connection2 and connection2.is_connected():
            connection2.close()
            connection2=None
    '''
    if watchlist_id == "0":
        return {"Content": [], "ID": "0"}, 200
    watchlist_object = ws.get_watchlist_by_id(watchlist_id)
    if utils.is_db_response_error(watchlist_object):
        return {'Error': str(watchlist_object)}, 404
    #utils.logging.debug(f"Isnt error in recomandation")
    # Extract TMDB IDs and is_movie from the watchlist object
    extracted_watchlist = [
        {
            'TMDB_ID': item.get('TMDB_ID'),
            'is_movie': item.get('is_movie'),
            'ID': item.get('ID'),
            'is_liked': item.get('is_liked')

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

 except Exception as e:
    # connection2.rollback()
     print(f"Transaction failed: in  update  {e}")
     return "0"
 finally:
     if 'cursor3' in locals() and cursor3:
         cursor3.close()
     if 'cursor4' in locals() and cursor4:
         cursor4.close()
     if 'connection2' in locals() and not(connection2 is None) :
         if connection2 and connection2.is_connected():
          connection2.close()
     semaphore.release()


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

def remove_user_prep_item(usr_prep,tmdb_id,is_movie):
    return [item for item in usr_prep if not (item["media_id"] == tmdb_id and item["is_movie"] == is_movie)]
def update_user_prep_item(usr_prep,tmdb_id,is_movie,is_liked,type):
    for p in usr_prep:
        if p["media_Id"] ==tmdb_id:
            p["is_liked"]= is_liked
            return usr_prep

    new={}
    new['media_Id']= tmdb_id
    new["is_movie"]=is_movie
    new["is_liked"]=is_liked
    new["type"]=type
    if is_movie==0:
        gen_str = get_tv_gen_by_id(api_key, tmdb_id)
        new['genres']= gen_str
        x = get_tv_keywords(api_key, tmdb_id)
        if "results" in x:
            new['key_words'] = x["results"]
    else :
        gen_str = get_movie_gen_by_id(api_key, tmdb_id)
        new['genres'] = gen_str
        x = get_movie_keywords(api_key, tmdb_id)
        if "results" in x:
            new['key_words'] = x["results"]
    usr_prep.append(new)
    return usr_prep


def get_usr_prep(usr_id):
   try:
    query = f"SELECT *  from rating where rating.User_ID = %s "
    connection2 = connection_pool.get_connection()
    cursor3 = connection2.cursor()
    cursor4 = connection2.cursor(dictionary=True)

    cursor4.execute(query, (usr_id,))


    rating_of_usr = cursor4.fetchall()
    usr_prefrence = []
    for r in rating_of_usr:
        if r['is_movie'] == 0:
            gen_str = get_tv_gen_by_id(api_key, r['media_ID'])
            r['genres'] = gen_str
            x = get_tv_keywords(api_key, r['media_ID'])
            if "results" in x:
                r['key_words'] = x["results"]
        elif r['is_movie'] == 1:
            gen_str = get_movie_gen_by_id(api_key, r['media_ID'])
            x = get_movie_keywords(api_key, r['media_ID'])
            if "results" in x:
                r['key_words'] = x["results"]
            r['genres'] = gen_str
        p = {}
        p["media_Id"] = r["media_ID"]
        p['gnr_str'] = r['genres']
        p['is_movie'] = r['is_movie']
        p['type']= "rating"
        if "key_words" in r:
            p['key_words'] = r['key_words']
        if r['rating'] >= 7:
            p['is_liked'] = 1
        else:
            p['is_liked'] = 0
        usr_prefrence.append(p)
    # return usr_prefrence
    query = f"SELECT *  from recommendation_info where user_ID = %s "

    cursor4.execute(query, (usr_id,))


    feedbackes = cursor4.fetchall()
    for r in feedbackes:
        if r['is_movie'] == 0:
            gen_str = get_tv_gen_by_id(api_key, r['media_id'])
            r['genres'] = gen_str
            x = get_tv_keywords(api_key, r['media_id'])
            if "results" in x:
                r['key_words'] = x["results"]
        elif r['is_movie'] == 1:
            gen_str = get_movie_gen_by_id(api_key, r['media_id'])
            r['genres'] = gen_str
            x = get_movie_keywords(api_key, r['media_id'])
            if "results" in x:
                r['key_words'] = x["results"]
        p = {}
        p["media_Id"] = r["media_id"]
        p['gnr_str'] = r['genres']
        p['is_movie'] = r['is_movie']
        p['type'] = "feedback"
        if "key_words" in r:
            p['key_words'] = r['key_words']
        if r['liked'] == 1:
            p['is_liked'] = 1
        else:
            p['is_liked'] = 0
        usr_prefrence.append(p)
    return usr_prefrence
   except Exception as e:
       return []
   finally:
       if 'cursor3' in locals() and cursor3:
           cursor3.close()
       if 'cursor4' in locals() and cursor4:
           cursor4.close()
       if 'connection2' in locals() and connection2.is_connected():
           connection2.close()


@recommendation_routes.route('/api/Media_recommendation', methods=['GET'])
@auth_required
def get_media_recommendationv2(token_info):
   try:
    x=[]
    print("starting recommendation process")
    fields_to_keep = ["title", "release_date", "vote_average", "Recommended_by", "trailer", "poster_path",
                      "overview", "name", "is_movie", "genres","tmdb_id", "original_title", "original_name", "first_air_date"]
    usr_id = token_info.get('sub')
    query = f"SELECT *  from rating where rating.User_ID = %s "
    connection2 = connection_pool.get_connection()
    cursor3 = connection2.cursor()
    cursor4 = connection2.cursor(dictionary=True)
    cursor4.execute(query, (usr_id,))

    rating_of_usr = cursor4.fetchall()
    '''
    query = f"SELECT *  from rating where rating.User_ID = %s "
    while 1:
     try:
      cursor2.execute(query, (usr_id,))
      break
     except Error as e:
         time.sleep(0.1)
    rating_of_usr = cursor2.fetchall()
    usr_prefrence = []
    for r in rating_of_usr:
        if r['is_movie'] == 0:
            gen_str = get_tv_gen_by_id(api_key, r['media_ID'])
            r['genres'] = gen_str
            x=get_tv_keywords(api_key, r['media_ID'])
            if "results" in x:
             r['key_words'] = x["results"]
        elif r['is_movie'] == 1:
            gen_str = get_movie_gen_by_id(api_key, r['media_ID'])
            x= get_movie_keywords(api_key, r['media_ID'])
            if "results" in x:
                r['key_words'] =x["results"]
            r['genres'] = gen_str
        p = {}
        p["media_Id"] = r["media_ID"]
        p['gnr_str'] = r['genres']
        p['is_movie'] = r['is_movie']
        if "key_words" in r:
         p['key_words'] = r['key_words']
        if r['rating'] >= 7:
            p['is_liked'] = 1
        else:
            p['is_liked'] = 0
        usr_prefrence.append(p)
    # return usr_prefrence
    query = f"SELECT *  from recommendation_info where user_ID = %s "
    while 1:
        try:
            cursor2.execute(query, (usr_id,))
            break
        except Error as e:
            time.sleep(0.1)
    feedbackes= cursor2.fetchall()
    for r in feedbackes:
        if r['is_movie'] == 0:
            gen_str = get_tv_gen_by_id(api_key, r['media_id'])
            r['genres'] = gen_str
            x = get_tv_keywords(api_key, r['media_id'])
            if "results" in x:
              r['key_words']= x["results"]
        elif r['is_movie'] == 1:
            gen_str = get_movie_gen_by_id(api_key, r['media_id'])
            r['genres'] = gen_str
            x = get_movie_keywords(api_key, r['media_id'])
            if "results" in x:
             r['key_words'] = x["results"]
        p = {}
        p["media_Id"] = r["media_id"]
        p['gnr_str'] = r['genres']
        p['is_movie'] = r['is_movie']
        if "key_words" in r:
         p['key_words'] = r['key_words']
        if r['liked'] == 1:
            p['is_liked'] = 1
        else:
            p['is_liked'] = 0
        usr_prefrence.append(p)
    '''
    '''
    if not  session.get('usr_pref',[])  :
        x = get_usr_prep(usr_id)
        session['usr_pref'] = x
        print("not in session")
    else:
        print("in session")


    usr_prefrence= session.get('usr_pref',[])
    '''
    usr_prefrence= get_usr_prep(usr_id)
    algo_recommendation = []
    key_words=[]

    for u in usr_prefrence:
        if "key_words" in u:
            if u["is_liked"] ==1:
             for x in u["key_words"]:
                key_words.append(x)

    counter = Counter((item['id'], item['name']) for item in key_words)

    key_words= [{'id': id, 'name': name, 'count': count} for (id, name), count in counter.items()]
    '''
    for k in key_words:
        movie_count = get_movie_count(api_key, k["id"])
        tv_count = get_tv_count(api_key, k["id"])
        k["results_count"] = movie_count + tv_count
    '''
    #key_words = [item for item in key_words if item['count'] > 1]
    chosen_words= []
    rating_len=len (rating_of_usr)
    for k in key_words:
        if k['count']>=rating_len/4:
            #chosen_words.append({'id': k['id'], 'name' : k['name']})
            chosen_words.append(k['id'])
    filter_key_words=[ [item for item in key_words if item['id'] not in chosen_words]]
    key_words=filter_key_words[0]
    sim=calculate_keyword_similarity(key_words)
    while len(sim) >1:
     o1=sim[0]
     if  o1['count1'] + o1['count2']  >=rating_len/4:
         chosen_words.append(o1['id1'])
         filtered_data = [item for item in sim if item['id1'] != o1['id1'] and item['id2'] != o1['id1']  and item['id1'] != o1['id2'] and item['id2'] != o1['id2'] ]
         sim= filtered_data
     else:
          newcount=o1['count1'] + o1['count2']
          filtered_data = [item for item in sim if item['id1'] != o1['id2'] and item['id2'] != o1['id2']]
          sim = filtered_data
          for s in sim:
              if s["id1"]==  o1['id1']:
                  s["count1"]= newcount
              if s["id2"]==  o1['id1']:
                  s["count2"] = newcount
    movies_canidate=[]
    tv_canidate=[]
    for w in chosen_words:
        movie_res= get_movies_by_keyword(w)
        tv_res= get_tv_shows_by_keyword(w)
        for m in movie_res:
            m["is_movie"]=1
            movies_canidate.append(m)
        for t in tv_res:
            t["is_movie"] = 1
            tv_canidate.append(t)
    algo_recommendation2=[]
    while 1:
        if len(algo_recommendation2)==5:
            break
        rnd= random.randint(1, 2)
        if rnd ==1:
            random_element = random.choice(movies_canidate)
            can_id=random_element["id"]
            exists_in_usr_pref = any(item["media_Id"] == can_id for item in usr_prefrence)
            exist_in_algo= any(item["id"] == can_id for item in algo_recommendation2)
            if exists_in_usr_pref or exist_in_algo:
                continue
            gen_str=""
            for g in random_element['genre_ids']:
                gen_str=gen_str +str(g)+ ','
            can_like, can_dislike = check_compatibility_v2(usr_prefrence, gen_str)
            if (can_like > can_dislike):
                can_copy = copy.deepcopy(random_element)
                can_copy["likelihood"] = can_like - can_dislike
                can_copy["is_movie"] = 1
                can_copy["Recommended_by"] = "Algorithm2"
                algo_recommendation2.append(can_copy)
        if rnd ==2:
            random_element = random.choice(tv_canidate)
            can_id=random_element["id"]
            exists_in_usr_pref = any(item["media_Id"] == can_id for item in usr_prefrence)
            exist_in_algo= any(item["id"] == can_id for item in algo_recommendation2)
            if exists_in_usr_pref or exist_in_algo:
                continue
            gen_str=""
            for g in random_element['genre_ids']:
                gen_str=gen_str +str(g)+ ','
            can_like, can_dislike = check_compatibility_v2(usr_prefrence, gen_str)
            if (can_like > can_dislike):
                can_copy = copy.deepcopy(random_element)
                can_copy["likelihood"] = can_like - can_dislike
                can_copy["is_movie"]=0
                can_copy["Recommended_by"] = "Algorithm2"
                algo_recommendation2.append(can_copy)


    while 1:
        if len(algo_recommendation) == 5:
            break
        can = greedy_random_selection(recommendation_candidates)
        can_gnr_str = ""
        can_media_id = can["media_ID"]

        # Check if can_media_id exists in usr_pref
        exists_in_usr_pref = any(item["media_Id"] == can_media_id for item in usr_prefrence)

        if exists_in_usr_pref:
            continue
        if (can["is_movie"]):
            can_gnr_str = get_movie_gen_by_id(api_key, can["media_ID"])
        else:
            can_gnr_str = get_tv_gen_by_id(api_key, can["media_ID"])
        can_like, can_dislike = check_compatibility_v2(usr_prefrence, can_gnr_str)
        if (can_like > can_dislike):
            can_copy = copy.deepcopy(can)
            can_copy["likelihood"] = can_like - can_dislike
            can_copy["Recommended_by"]= "Algorithm1"
            algo_recommendation.append(can_copy)
    return_arr = []
    join_algo=[]
    for a in algo_recommendation:
        join_algo.append(a)
    for a in algo_recommendation2:
        join_algo.append(a)
    join_algo=sorted(join_algo, key=lambda a: a["likelihood"], reverse=True)
    for a in  join_algo:
        if a["Recommended_by"] =="Algorithm1":
            if a["is_movie"]:
                info = get_movie_info(a["media_ID"])
                t = get_movie_trailer(a["media_ID"])
                info["trailer"] = t
                info["Recommended_by"] = "Popularity"
                info["is_movie"] = 1
                info["tmdb_id"] = a["media_ID"]
                info = filter_fields(info, fields_to_keep)
                info["streaming_services"] = media_page_streaming_services(a["media_ID"], "movie")
                info["user_id"] = "0"
                info["user_rating"] = 0
                info["video_links"] = []
                info["item_id"] = "0"
                info["list_id"] = None
                info["tmdb_rating"] = info.get("vote_average")
                if not info.get("poster_path"):
                    info["poster_path"] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
                    info["small_poster_path"] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
                else:
                    info["small_poster_path"] = "https://image.tmdb.org/t/p/w200/" + info[
                        "poster_path"]
                    info["poster_path"] = "https://image.tmdb.org/t/p/original/" + info[
                        "poster_path"]
                return_arr.append(info)
            else:
                info = get_tv_show_info(a["media_ID"])
                t = get_tv_trailer(a["media_ID"])
                info["trailer"] = t
                info["title"] = info.get("name")
                info["Recommended_by"] = "Popularity"
                info["is_movie"] = 0
                info["tmdb_id"] = a["media_ID"]
                info = filter_fields(info, fields_to_keep)
                info["streaming_services"] = media_page_streaming_services(a["media_ID"], "tv")
                info["user_id"] = "0"
                info["user_rating"] = 0
                info["video_links"] = []
                info["release_date"] = info.get('first_air_date')
                info["item_id"] = "0"
                info["list_id"] = None
                info["tmdb_rating"] = info.get("vote_average")
                if not ("poster_path" in info):
                    info["poster_path"] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
                    info["small_poster_path"] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
                else:
                    info["small_poster_path"] = "https://image.tmdb.org/t/p/w200/" + info[
                        "poster_path"]
                    info["poster_path"] = "https://image.tmdb.org/t/p/original/" + info[
                        "poster_path"]
                return_arr.append(info)
        if a["Recommended_by"] == "Algorithm2":
            if a["is_movie"]:
                info = get_movie_info(a["id"])
                t = get_movie_trailer(a["id"])
                info["trailer"] = t
                info["Recommended_by"] = "Key words"
                info["is_movie"] = 1
                info["tmdb_id"] = a["id"]
                info = filter_fields(info, fields_to_keep)
                info["streaming_services"] = media_page_streaming_services(a["id"], "movie")
                info["user_id"] = "0"
                info["user_rating"] = 0
                info["video_links"] = []
                info["item_id"] = "0"
                info["list_id"] = None
                info["tmdb_rating"] = info.get("vote_average")
                # TODO missing the default path, doesn't protect against no image....
                if not ("poster_path" in info):
                    info["poster_path"] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
                    info["small_poster_path"] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
                else:
                    info["small_poster_path"] = "https://image.tmdb.org/t/p/w200/" + str(info["poster_path"])
                    info["poster_path"] = "https://image.tmdb.org/t/p/original/" + str(info["poster_path"])
                return_arr.append(info)
            else:
                info = get_tv_show_info(a["id"])
                t = get_tv_trailer(a["id"])
                info["trailer"] = t
                info["title"] = info.get("name")
                info["Recommended_by"] = "Key words"
                info["is_movie"] = 0
                info["tmdb_id"] = a["id"]
                info = filter_fields(info, fields_to_keep)
                info["streaming_services"] = media_page_streaming_services(a["id"], "tv")
                info["user_id"] = "0"
                info["user_rating"] = 0
                info["video_links"] = []
                info["release_date"] = info.get('first_air_date')
                info["item_id"] = "0"
                info["list_id"] = None
                info["tmdb_rating"] = info.get("vote_average")
                if not ("poster_path" in info):
                    info["poster_path"] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
                    info["small_poster_path"] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
                else:
                    info["small_poster_path"] = "https://image.tmdb.org/t/p/w200/" + str(info[ "poster_path"])
                    info["poster_path"] = "https://image.tmdb.org/t/p/original/" + str(info["poster_path"])
                return_arr.append(info)
        if len(return_arr) >5:
         break
    return return_arr


    for a in algo_recommendation:

        if a["is_movie"]:
            info = get_movie_info(a["media_ID"])
            t = get_movie_trailer(a["media_ID"])
            info["trailer"] = t
            info["Recommended_by"] = "Algorithm1"
            info["is_movie"] = 1
            info["tmdb_id"]= a["media_ID"]
            info = filter_fields(info, fields_to_keep)
            info["streaming_services"] = media_page_streaming_services(a["media_ID"], "movie")
            info["user_id"] = "0"
            info["user_rating"] = 0
            info["video_links"] = []
            info["item_id"] = "0"
            info["list_id"] = None
            info["tmdb_rating"] = info.get("vote_average")
            if not info["poster_path"]:
                info["poster_path"] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
                info["small_poster_path"] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
            else:
             info["small_poster_path"] = "https://image.tmdb.org/t/p/w200/" + info[
                "poster_path"]
             info["poster_path"] = "https://image.tmdb.org/t/p/original/" + info[
                "poster_path"]
        else:
            info = get_tv_show_info(a["media_ID"])
            t = get_tv_trailer(a["media_ID"])
            info["trailer"] = t
            info["title"] = info.get("name")
            info["Recommended_by"] = "Algorithm1"
            info["is_movie"] = 0
            info["tmdb_id"] = a["media_ID"]
            info = filter_fields(info, fields_to_keep)
            info["streaming_services"] = media_page_streaming_services(a["media_ID"], "tv")
            info["user_id"] = "0"
            info["user_rating"] = 0
            info["video_links"] = []
            info["release_date"] = info.get('first_air_date')
            info["item_id"] = "0"
            info["list_id"] = None
            info["tmdb_rating"] = info.get("vote_average")
            if not ("poster_path" in info):
                info["poster_path"] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
                info["small_poster_path"] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
            else:
             info["small_poster_path"] = "https://image.tmdb.org/t/p/w200/" + info[
                "poster_path"]
             info["poster_path"] = "https://image.tmdb.org/t/p/original/" + info[
                "poster_path"]
        return_arr.append(info)
    for a in algo_recommendation2:
        if a["is_movie"]:
            info = get_movie_info(a["id"])
            t = get_movie_trailer(a["id"])
            info["trailer"] = t
            info["recommended_by"] = "Algorithm2"
            info["is_movie"] = 1
            info["tmdb_id"]= a["id"]
            info = filter_fields(info, fields_to_keep)
            info["streaming_services"] = media_page_streaming_services(a["id"], "movie")
            info["user_id"] = "0"
            info["user_rating"] = 0
            info["video_links"] = []
            info["item_id"] = "0"
            info["list_id"] = None
            info["tmdb_rating"] = info.get("vote_average")
            # TODO missing the default path, doesn't protect against no image....
            if not ("poster_path" in info):
                info["poster_path"] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
                info["small_poster_path"] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
            else:
             info["small_poster_path"] = "https://image.tmdb.org/t/p/w200/" + info[
                "poster_path"]
             info["poster_path"] = "https://image.tmdb.org/t/p/original/" + info[
                "poster_path"]
        else:
            info = get_tv_show_info(a["id"])
            t = get_tv_trailer(a["id"])
            info["trailer"] = t
            info["title"] = info.get("name")
            info["Recommended_by"] = "Algorithm2"
            info["is_movie"] = 0
            info["tmdb_id"] = a["id"]
            info = filter_fields(info, fields_to_keep)
            info["streaming_services"] = media_page_streaming_services(a["id"], "tv")
            info["user_id"] = "0"
            info["user_rating"] = 0
            info["video_links"] = []
            info["release_date"] = info.get('first_air_date')
            info["item_id"] = "0"
            info["list_id"] = None
            info["tmdb_rating"] = info.get("vote_average")
            if not info.get("poster_path"):
                info["poster_path"] = "https://i.postimg.cc/fRV5SqCb/default-movie.jpg"
                info["small_poster_path"] = "https://i.postimg.cc/TPrVnzDT/default-movie-small.jpg"
            else:
             info["poster_path"] = "https://image.tmdb.org/t/p/original/" + info[
                "poster_path"]
             info["small_poster_path"] = "https://image.tmdb.org/t/p/w200/" + info[
                "poster_path"]
        return_arr.append(info)
        if len(return_arr) >10:
         break
    #print("the return arr is" , return_arr)
    return return_arr
   except Exception as e:
       print (str(e))
       return []

   finally:
       if 'cursor3' in locals() and cursor3:
           cursor3.close()
       if 'cursor4' in locals() and cursor4:
           cursor4.close()
       if 'connection2' in locals() and connection2.is_connected():
           connection2.close()
