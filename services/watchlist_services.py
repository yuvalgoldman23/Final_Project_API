from database_connector import connection, cursor, cursor2
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify


def add_watch_list_item(userID, Media_TMDB_ID, Parent_ID, is_movie):
    print("in db-side add watchlist item")
    watchlist_id_query = "SELECT ID FROM final_project_db.watch_lists_objects WHERE User_ID = %s AND TMDB_ID = %s AND Parent_ID = %s AND is_movie = %s ORDER BY ID DESC LIMIT 1"

    try:
        select_query = "SELECT COUNT(*) FROM final_project_db.watch_lists_objects WHERE TMDB_ID = %s AND Parent_ID = %s AND User_ID = %s AND is_movie = %s"

        with connection.cursor() as cursor:
            cursor.execute(select_query, (Media_TMDB_ID, Parent_ID, userID, is_movie))
            result = cursor.fetchall()[0]
            #print("in result phase, result is " + str(result[0]))

            if result[0] == 0:
                print("successfully added " + str(Media_TMDB_ID) + " to watchlist")
                insert_query = "INSERT INTO final_project_db.watch_lists_objects(User_ID,TMDB_ID,Parent_ID, is_movie) VALUES (%s,%s,%s, %s)"
                cursor.execute(insert_query, (userID, Media_TMDB_ID, Parent_ID, is_movie))
                connection.commit()

                cursor.execute(watchlist_id_query, (userID, Media_TMDB_ID, Parent_ID, is_movie))
                main_watchlist_id = cursor.fetchall()[0][0]
                print("Added movie {} to watchlist {}".format(Media_TMDB_ID, Parent_ID))
                print("in successful addition phase with returned id of ", main_watchlist_id)
                return main_watchlist_id, 201
            else:
                print("Content already in watchlist")
                return "Content already in watchlist", 204
    except mysql.connector.Error as err:
        return handle_mysql_error(err)


def remove_watch_list_item(userID, watch_list_id, content_id):
    try:
        delete_query = "DELETE FROM final_project_db.watch_lists_objects WHERE Parent_ID= %s AND TMDB_ID = %s AND User_ID= %s ;"

        with connection.cursor() as cursor:
            cursor.execute(delete_query, (watch_list_id, content_id, userID))
            connection.commit()
            if cursor.rowcount > 0:
                print(f"Deletion of watchlist item {content_id} successful")
                return jsonify({"type": "success", "message": f"Removed item {content_id}"}), 200
            else:
                return jsonify({"type": "Failure",
                                "message": "No item deleted. Please make sure it belongs to the logged-in user"}), 200
    except mysql.connector.Error as err:
        return handle_mysql_error(err)


def create_watchlist(user_id, name, Is_main):
    watchlist_id_query = "SELECT ID FROM final_project_db.watch_lists_names WHERE User_ID = %s ORDER BY ID DESC LIMIT 1"

    try:
        with connection.cursor() as cursor:
            if Is_main:
                query = "SELECT EXISTS(SELECT 1 FROM final_project_db.watch_lists_names WHERE User_ID = %s AND Main= %s)"
                cursor.execute(query, (user_id, True))
                exists = cursor.fetchall()[0][0]

                if not exists:
                    insert_query = "INSERT INTO final_project_db.watch_lists_names (User_ID, name, Main) VALUES (%s, %s, %s)"
                    cursor.execute(insert_query, (user_id, 'Main', True))
                    connection.commit()
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
                connection.commit()

                cursor.execute(watchlist_id_query, (user_id,))
                new_id = cursor.fetchall()[0][0]
                return new_id
    except mysql.connector.Error as err:
        return handle_mysql_error(err)


def remove_watch_list(userID, watch_list_id):
    try:
        with connection.cursor() as cursor:
            delete_query1 = "DELETE FROM final_project_db.watch_lists_names WHERE ID= %s AND User_ID= %s ;"
            cursor.execute(delete_query1, (watch_list_id, userID))
            connection.commit()

            if cursor.rowcount > 0:
                delete_query2 = "DELETE FROM final_project_db.watch_lists_objects WHERE Parent_ID= %s AND User_ID= %s ;"
                cursor.execute(delete_query2, (watch_list_id, userID))
                connection.commit()
                print(f"Deletion of watchlist {watch_list_id} successful")
                return jsonify({"type": "success", "message": f"Removed watchlist {watch_list_id}"}), 200
            else:
                return jsonify({"type": "Failure",
                                "message": "No watchlist deleted. Please make sure it belongs to the logged-in user"}), 200
    except mysql.connector.Error as err:
        return handle_mysql_error(err)


def get_user_watchlists(user_id):
    try:
        query = "SELECT * FROM final_project_db.watch_lists_names WHERE User_ID = %s"
        with connection.cursor(dictionary=True) as cursor2:
            cursor2.execute(query, (user_id,))
            return cursor2.fetchall()  # Keeping fetchall() as it is for this case
    except mysql.connector.Error as err:
        return handle_mysql_error(err)

def get_watchlist_by_id(watchlist_ID):
    """

    :param watchlist_ID:
    :return: Returns the content objects (tmdb_id's and is_movie) of the provided watchlist id
    """
    try:
        query = "SELECT * FROM final_project_db.watch_lists_objects WHERE Parent_ID = %s"
        with connection.cursor(dictionary=True) as cursor2:
            cursor2.execute(query, (watchlist_ID,))
            results = cursor2.fetchall()
            return results
    except mysql.connector.Error as err:
        return handle_mysql_error(err)


def get_watchlist_details_only(watchlist_ID):
    try:
        query = "SELECT * FROM final_project_db.watch_lists_names WHERE ID = %s"
        with connection.cursor(dictionary=True) as cursor2:
            cursor2.execute(query, (watchlist_ID,))
            results = cursor2.fetchall()  # Fetching all results

            return results[0] if results else None  # Maintaining original behavior
    except mysql.connector.Error as err:
        return handle_mysql_error(err)


def get_main_watchlist(user_ID):
    try:
        query = "SELECT * FROM final_project_db.watch_lists_names WHERE User_ID = %s AND Main = 1"
        with connection.cursor(dictionary=True) as cursor2:
            cursor2.execute(query, (user_ID,))
            results = cursor2.fetchall()  # Maintaining return type
            return results
    except mysql.connector.Error as err:
        return handle_mysql_error(err)


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
