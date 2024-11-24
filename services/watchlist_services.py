#from database_connector import connection, cursor, cursor2 , connection_pool, semaphore,global_lock
from database_connector import  connection_pool , semaphore
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify
import threading

import safety
lock = threading.Lock()

def add_watch_list_item(userID, Media_TMDB_ID, Parent_ID, is_movie):
    if not (safety.is_only_numbers_or_letters(userID) and safety.is_only_numbers_or_letters(Media_TMDB_ID)and safety.is_only_numbers_or_letters(Parent_ID) and safety.is_one_or_zero(is_movie)):
        return []
    print("in db-side add watchlist item")
    watchlist_id_query = "SELECT ID FROM final_project_db.watch_lists_objects WHERE User_ID = %s AND TMDB_ID = %s AND Parent_ID = %s AND is_movie = %s ORDER BY ID DESC LIMIT 1"

    try:
        select_query = "SELECT COUNT(*) FROM final_project_db.watch_lists_objects WHERE TMDB_ID = %s AND Parent_ID = %s AND User_ID = %s AND is_movie = %s"
        connection2 = connection_pool.get_connection()
        #cursor3 = connection2.cursor()
        #cursor4 = connection2.cursor(dictionary=True)
        if not connection2.is_connected():
            connection2.reconnect()

        with connection2.cursor() as cursor3:
            cursor3.execute(select_query, (Media_TMDB_ID, Parent_ID, userID, is_movie))
            result = cursor3.fetchall()[0]
            #print("in result phase, result is " + str(result[0]))

            if result[0] == 0:
                print("successfully added " + str(Media_TMDB_ID) + " to watchlist")
                insert_query = "INSERT INTO final_project_db.watch_lists_objects(User_ID,TMDB_ID,Parent_ID, is_movie) VALUES (%s,%s,%s, %s)"
                cursor3.execute(insert_query, (userID, Media_TMDB_ID, Parent_ID, is_movie))
                connection2.commit()

                cursor3.execute(watchlist_id_query, (userID, Media_TMDB_ID, Parent_ID, is_movie))
                main_watchlist_id = cursor3.fetchall()[0][0]
                print("Added movie {} to watchlist {}".format(Media_TMDB_ID, Parent_ID))
                print("in successful addition phase with returned id of ", main_watchlist_id)
                return main_watchlist_id, 201
            else:
                print("Content already in watchlist")
                return "Content already in watchlist", 204
    except mysql.connector.Error as err:
        return handle_mysql_error(err)
    finally:
        if 'cursor3' in locals() and cursor3:
            cursor3.close()
        if 'cursor4' in locals() and cursor4:
            cursor4.close()
        if 'connection2' in locals() and connection2.is_connected():
            connection2.close()



def remove_watch_list_item(userID, watch_list_id, content_id):
    if not (safety.is_only_numbers_or_letters(userID) and safety.is_only_numbers_or_letters(watch_list_id) and safety.is_only_numbers_or_letters(content_id)):
        return []
    try:
        delete_query = "DELETE FROM final_project_db.watch_lists_objects WHERE Parent_ID= %s AND TMDB_ID = %s AND User_ID= %s ;"
        connection2 = connection_pool.get_connection()
        #cursor3 = connection2.cursor()
        #cursor4 = connection2.cursor(dictionary=True)
        if not connection2.is_connected():
            connection2.reconnect()
        with connection2.cursor() as cursor:
            cursor.execute(delete_query, (watch_list_id, content_id, userID))
            connection2.commit()
            if cursor.rowcount > 0:
                print(f"Deletion of watchlist item {content_id} successful")
                return jsonify({"type": "success", "message": f"Removed item {content_id}"}), 200
            else:
                return jsonify({"type": "Failure",
                                "message": "No item deleted. Please make sure it belongs to the logged-in user"}), 200
    except mysql.connector.Error as err:
        return handle_mysql_error(err)
    finally:
        if 'cursor3' in locals() and cursor3:
            cursor3.close()
        if 'cursor4' in locals() and cursor4:
            cursor4.close()
        if 'connection2' in locals() and connection2.is_connected():
            connection2.close()



def create_watchlist(user_id, name, Is_main):
    watchlist_id_query = "SELECT ID FROM final_project_db.watch_lists_names WHERE User_ID = %s ORDER BY ID DESC LIMIT 1"
    if not (safety.is_only_numbers_or_letters(user_id),safety.is_only_numbers_or_letters(name),safety.is_one_or_zero(Is_main)):
        return []
    try:
        connection2 = connection_pool.get_connection()
        #cursor3 = connection2.cursor()
        #cursor4 = connection2.cursor(dictionary=True)
        if not connection2.is_connected():
            connection2.reconnect()
        with connection2.cursor() as cursor:
            if Is_main:
                query = "SELECT EXISTS(SELECT 1 FROM final_project_db.watch_lists_names WHERE User_ID = %s AND Main= %s)"
                cursor.execute(query, (user_id, True))
                exists = cursor.fetchall()[0][0]

                if not exists:
                    insert_query = "INSERT INTO final_project_db.watch_lists_names (User_ID, name, Main) VALUES (%s, %s, %s)"
                    cursor.execute(insert_query, (user_id, 'Main', True))
                    connection2.commit()
                    print(f"ID {user_id} list was added to the table.")

                    cursor.execute(watchlist_id_query, (user_id,))
                    main_watchlist_id = cursor.fetchall()[0][0]
                    print("new main watchlist id is", main_watchlist_id)
                    return main_watchlist_id
                else:
                    print(f"ID {user_id} list main watchlist already exists in the table.")
                    return f"ID {user_id} list main watchlist already exists in the table.", 201
            else:
                insert_query = "INSERT INTO final_project_db.watch_lists_names (User_ID,name,Main) VALUES (%s,%s,%s)"
                cursor.execute(insert_query, (user_id, name, False))
                connection2.commit()

                cursor.execute(watchlist_id_query, (user_id,))
                new_id = cursor.fetchall()[0][0]
                return new_id
    except mysql.connector.Error as err:
        return handle_mysql_error(err)
    finally:
        if 'cursor3' in locals() and cursor3:
            cursor3.close()
        if 'cursor4' in locals() and cursor4:
            cursor4.close()
        if 'connection2' in locals() and connection2.is_connected():
            connection2.close()



def remove_watch_list(userID, watch_list_id):
    if not (safety.is_only_numbers_or_letters(userID) and safety.is_only_numbers_or_letters(watch_list_id)):
        return []
    try:
        connection2 = connection_pool.get_connection()
        #cursor3 = connection2.cursor()
        #cursor4 = connection2.cursor(dictionary=True)
        if not connection2.is_connected():
            connection2.reconnect()
        with connection2.cursor() as cursor:
            delete_query1 = "DELETE FROM final_project_db.watch_lists_names WHERE ID= %s AND User_ID= %s ;"
            cursor.execute(delete_query1, (watch_list_id, userID))
            connection2.commit()

            if cursor.rowcount > 0:
                delete_query2 = "DELETE FROM final_project_db.watch_lists_objects WHERE Parent_ID= %s AND User_ID= %s ;"
                cursor.execute(delete_query2, (watch_list_id, userID))
                connection2.commit()
                print(f"Deletion of watchlist {watch_list_id} successful")
                return jsonify({"type": "success", "message": f"Removed watchlist {watch_list_id}"}), 200
            else:
                return jsonify({"type": "Failure",
                                "message": "No watchlist deleted. Please make sure it belongs to the logged-in user"}), 200
    except mysql.connector.Error as err:
        return handle_mysql_error(err)
    finally:
        if 'cursor3' in locals() and cursor3:
            cursor3.close()
        if 'cursor4' in locals() and cursor4:
            cursor4.close()
        if 'connection2' in locals() and connection2.is_connected():
            connection2.close()



def get_user_watchlists(user_id):

    try:

        query = "SELECT * FROM final_project_db.watch_lists_names WHERE User_ID = %s"
        connection2 = connection_pool.get_connection()
        #cursor3 = connection2.cursor()
        #cursor4 = connection2.cursor(dictionary=True)
        if not connection2.is_connected():
            connection2.reconnect()
        with connection2.cursor(dictionary=True) as cursor2:
            cursor2.execute(query, (user_id,))
            return cursor2.fetchall()  # Keeping fetchall() as it is for this case
    except mysql.connector.Error as err:
        return handle_mysql_error(err)
    finally:
        if 'cursor3' in locals() and cursor3:
            cursor3.close()
        if 'cursor4' in locals() and cursor4:
            cursor4.close()
        if 'connection2' in locals() and connection2.is_connected():
            connection2.close()


def get_watchlist_by_id(watchlist_ID):
    if not(safety.is_only_numbers_or_letters(watchlist_ID)):
         return []

    try:
            # Thread-safe access
            # Fetch connection from pool
            connection2 = connection_pool.get_connection()

            # Ensure connection is alive
            if not connection2.is_connected():
                connection2.reconnect()

            # Execute query
            query = """
            SELECT 
                wlo.ID,
                wlo.Parent_ID,
                wlo.TMDB_ID,
                wlo.User_ID,
                wlo.is_movie,
                CASE 
                    WHEN ri.liked = 1 THEN 1
                    ELSE 0
                END AS is_liked
            FROM 
                watch_lists_objects wlo
            LEFT JOIN 
                recommendation_info ri
            ON 
                wlo.TMDB_ID = ri.media_id 
                AND wlo.is_movie = ri.is_movie 
                AND wlo.User_ID = ri.user_ID
            WHERE 
                wlo.Parent_ID = %s;
            """
            with connection2.cursor(dictionary=True) as cursor4:
                cursor4.execute(query, (watchlist_ID,))
                results = cursor4.fetchall()

            return results

    except mysql.connector.Error as err:

        return handle_mysql_error(err)

    finally:
        # Ensure connection is returned to pool
        if 'connection2' in locals() and connection2.is_connected():
            connection2.close()


def get_watchlist_details_only(watchlist_ID):
    if not (safety.is_only_numbers_or_letters(watchlist_ID)):
        return []

    try:
        query = "SELECT * FROM final_project_db.watch_lists_names WHERE ID = %s"
        connection2 = connection_pool.get_connection()
        #cursor3 = connection2.cursor()
        #cursor4 = connection2.cursor(dictionary=True)
        if not connection2.is_connected():
            connection2.reconnect()
        with connection2.cursor(dictionary=True) as cursor2:
            cursor2.execute(query, (watchlist_ID,))
            results = cursor2.fetchall()  # Fetching all results

            return results[0] if results else None  # Maintaining original behavior
    except mysql.connector.Error as err:
        print ("filed in ws")
        return handle_mysql_error(err)
    finally:
        if 'cursor3' in locals() and cursor3:
            cursor3.close()
        if 'cursor4' in locals() and cursor4:
            cursor4.close()
        if 'connection2' in locals() and connection2.is_connected():
            connection2.close()



def get_main_watchlist(user_ID):


    try:
        query = "SELECT * FROM final_project_db.watch_lists_names WHERE User_ID = %s AND Main = 1"
        connection2 = connection_pool.get_connection()
        if not connection2.is_connected():
            connection2.reconnect()
        #cursor3 = connection2.cursor()
        #cursor4 = connection2.cursor(dictionary=True)
        with connection2.cursor(dictionary=True) as cursor2:
            cursor2.execute(query, (user_ID,))
            results = cursor2.fetchall()  # Maintaining return type
            return results
    except mysql.connector.Error as err:
        return handle_mysql_error(err)
    finally:
        if 'cursor3' in locals() and cursor3:
            cursor3.close()
        if 'cursor4' in locals() and cursor4:
            cursor4.close()
        if 'connection2' in locals() and connection2.is_connected():
            connection2.close()


def handle_mysql_error(err):
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your username or password")
        return err
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
        return err
    else:
        print(err)
        return err


def check_content_in_watchlist(watchlist_ID, content_id, is_movie):
    """
    Check if a specific content ID and is_movie flag exist in the given watchlist.

    :param watchlist_ID: The ID of the watchlist to check.
    :param content_id: The content ID to search for.
    :param is_movie: Boolean flag indicating if the content is a movie.
    :return: True if the content exists in the watchlist, otherwise False.
    """
    if not (safety.is_only_numbers_or_letters(watchlist_ID)and safety.is_only_numbers_or_letters(content_id) and safety.is_one_or_zero(is_movie)):
        return []
    try:
        query = """
        SELECT COUNT(*) AS count 
        FROM final_project_db.watch_lists_objects 
        WHERE Parent_ID = %s AND TMDB_ID = %s AND is_movie = %s
        """
        connection2 = connection_pool.get_connection()
        #cursor3 = connection2.cursor()
        #cursor4 = connection2.cursor(dictionary=True)
        with connection2.cursor(dictionary=True) as cursor2:
            cursor2.execute(query, (watchlist_ID, content_id, is_movie))
            result = cursor2.fetchone()
            return result['count'] > 0, 200  # Return True if count is greater than 0, otherwise False
    except mysql.connector.Error as err:
        return handle_mysql_error(err), 400
    finally:
        if 'cursor3' in locals() and cursor3:
            cursor3.close()
        if 'cursor4' in locals() and cursor4:
            cursor4.close()
        if 'connection2' in locals() and connection2.is_connected():
            connection2.close()


