from database_connector import connection, cursor, cursor2
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify




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


def add_watch_list(user_id,name,Is_main):
    try:
     if (Is_main):
         query = f"SELECT EXISTS(SELECT 1 FROM `final_project_db`.`users` WHERE User_ID = %s AND Main= %s)"
         cursor.execute(query, (user_id,True))
         exists = cursor.fetchone()[0]

         if not exists:
             # Insert the ID if it does not exist
             insert_query = f"INSERT INTO `final_project_db`.`watch_lists_names` User_ID,name,Main) VALUES (%s,%s,%s)"
             cursor.execute(insert_query, (user_id,"Main",True ))
             connection.commit()
             print(f"ID {user_id}  list was added to the table .")
             return jsonify({"ID {user_id}  list was added to the table ."}), 404
         else:
             print(f"ID {user_id}  list mainalready exists in the table .")
     else :
         insert_query = f"INSERT INTO `final_project_db`.`watch_lists_names` (User_ID,name,Main) VALUES (%s,%s,%s)"
         cursor.execute(insert_query, (user_id, name, False))
         connection.commit()
	except mysql.connector.Error as err:

        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:

            print("Something is wrong with your user name or password")
            return jsonify({"Something is wrong with your user name or password"}), 404

        elif err.errno == errorcode.ER_BAD_DB_ERROR:

            print("Database does not exist")
            return jsonify({"Database does not exist"}), 404

        else:
            print(err)
            return err
def remove_watch_list_item(userID,watch_list_item_id):
    try:
        delete_query = "DELETE FROM `final_project_db`.`watch_lists_objects` WHERE `ID`= %s AND `User_ID`= %s ;"
        cursor.execute(delete_query, (watch_list_item_id, userID))
        connection.commit()
        return jsonify({"Complited"})
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return jsonify({"Something is wrong with your user name or password"}), 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return jsonify({"Database does not exist"}), 404
        else:
            print(err)
            return err



def remove_watch_list(userID,watch_list_item_id):
    try:
        delete_query1 = "DELETE FROM `final_project_db`.`watch_lists_names` WHERE `ID`= %s AND `User_ID`= %s ;"

        cursor.execute(delete_query1, (watch_list_item_id, userID))
        delete_query2 = "DELETE FROM `final_project_db`.`watch_lists_objects` WHERE `Parent_ID`= %s AND `User_ID`= %s ;"
        cursor.execute(delete_query2, (watch_list_item_id, userID))
        connection.commit()
        return jsonify({"Complited"})
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return jsonify({"Something is wrong with your user name or password"}), 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return jsonify({"Database does not exist"}), 404
        else:
            print(err)
            return err

