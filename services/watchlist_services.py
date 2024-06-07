from database_connector import connection, cursor, cursor2
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify

def get_user_watchlist(user_id):
    try:

        query = f"SELECT * FROM `final_project_db`.`watch_list` WHERE Owner_ID = %s"
        cursor2.execute(query, (user_id,))
        return jsonify(cursor2.fetchall()), 200

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            return jsonify({"Something is wrong with your user name or password"}), 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            return jsonify({"Database does not exist"}), 404
        else:
            return err


def add_watch_list_item(user_id, media_tmdb_id, is_movie, comment, is_watched, rating, progress):
    try:
        insert_query = f"INSERT INTO `final_project_db`.`watch_list`(`Owner_ID`,`Media_ID`,`Is_Movie`,`Comment`,`Watched`,`Rating`,`progress`) VALUES (%s,%s,%s,%s,%s,%s,%s) "
        cursor.execute(insert_query, (user_id, media_tmdb_id, is_movie, comment, is_watched, rating, progress))
        connection.commit()
        return jsonify({"Success": f"Added item {media_tmdb_id} to watchlist"}), 200
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            return jsonify({"Something is wrong with your user name or password"}), 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            return jsonify({"Database does not exist"}), 404
        else:
            return jsonify({err}), 404


def remove_watch_list_item(user_id, watch_list_item_id):
    try:
        delete_query = "DELETE FROM `final_project_db`.`reviews` WHERE `ID`= %s AND `Writer_ID`= %s ;"
        cursor.execute(delete_query, (watch_list_item_id, user_id))
        connection.commit()
        return jsonify({"Success": f"Removed item {watch_list_item_id} from watchlist"}), 200
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            return jsonify({"Something is wrong with your user name or password"}), 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            return jsonify({"Database does not exist"}), 404
        else:
            return jsonify({err}), 404


def update_watched_status(watch_item_id, user_id, watched_value):
    try:
        update_query = "UPDATE FROM `final_project_db`.`watch_list` SET `Prpgress`=%s WHERE `ID`= %s AND `Owner_ID`= %s ;"
        cursor.execute(update_query, (watched_value, watch_item_id, user_id))
        connection.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def update_rating(watch_item_id, user_id, rating):
    try:
        update_query = "UPDATE FROM `final_project_db`.`watch_list` SET `Rating`=%s WHERE `ID`= %s AND `Owner_ID`= %s ;"
        cursor.execute(update_query, (rating, watch_item_id, user_id))
        connection.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    t = 6


def update_comment(watch_item_id, user_id, comment):
    try:
        update_query = "UPDATE FROM `final_project_db`.`watch_list` SET `Comment`=%s WHERE `ID`= %s AND `Owner_ID`= %s ;"
        cursor.execute(update_query, (comment, watch_item_id, user_id))
        connection.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    t = 6
    t = 5


def update_progress(watch_item_id, user_id, progress):
    try:
        update_query = "UPDATE FROM `final_project_db`.`watch_list` SET `Progress`=%s WHERE `ID`= %s AND `Owner_ID`= %s ;"
        cursor.execute(update_query, (progress, watch_item_id, user_id))
        connection.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    t = 6
