from database_connector import connection, cursor, cursor2
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify




def add_watch_list_item(userID,Media_TMDB_ID,Parent_ID, is_movie):
    print("in db-side add watchlist item")
    # Query to get the last inserted id for the given user_id
    watchlist_id_query = "SELECT ID FROM `final_project_db`.`watch_lists_objects` WHERE User_ID = %s AND TMDB_ID = %s AND `Parent_ID` = %s AND is_movie = %s ORDER BY ID DESC LIMIT 1"
    try:
        select_query = "SELECT COUNT(*) FROM `final_project_db`.`watch_lists_objects` WHERE `TMDB_ID` = %s AND `Parent_ID` = %s;"
        # Execute the SELECT query
        cursor.execute(select_query, (Media_TMDB_ID, Parent_ID))
        result = cursor.fetchone()
        print("in result phase, result is " + str(result))
        # Successfully added content to watchlist, now return its ID
        if result[0] == 0:
            print("successfully added " + str(Media_TMDB_ID) + " to watchlist")
            insert_query = f"INSERT INTO `final_project_db`.`watch_lists_objects`(`User_ID`,`TMDB_ID`,`Parent_ID`, `is_movie`) VALUES (%s,%s,%s, %s) "
            cursor.execute(insert_query, (userID,Media_TMDB_ID ,Parent_ID, is_movie))
            connection.commit()
            cursor.execute(watchlist_id_query, (userID, Media_TMDB_ID, Parent_ID, is_movie))
            main_watchlist_id = cursor.fetchone()[0]
            print("Added movie {} to watchlist {}".format(Media_TMDB_ID, Parent_ID))
            print("in successful addition phase with returned id of " , main_watchlist_id)
            return main_watchlist_id, 201
        else:
            print("Content already in watchlist")
            return "Content already in watchlist", 204
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return jsonify({"type":"Error" , "message:": "Something is wrong with your user name or password"})
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return jsonify({ "type":"Error" ,"message:": "Database does not exist"})
        else:
            print("DB Error:", err)
            return err



def remove_watch_list_item(userID,watch_list_id, content_id):
    try:
        delete_query = "DELETE FROM `final_project_db`.`watch_lists_objects` WHERE `Parent_ID`= %s AND `TMDB_ID` = %s AND `User_ID`= %s ;"
        cursor.execute(delete_query, (watch_list_id, content_id, userID))
        connection.commit()
        if cursor.rowcount > 0:
            print(f"Deletion of watchlist item {content_id} successful")
            return jsonify({"type": "success", "message": f"Removed item {content_id}"}), 200
        else:
            return jsonify({"type": "Failure", "message": "No item deleted. Please make sure it belongs to the logged in user"}), 200
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return jsonify({"type":"Error" ,"message:": "Something is wrong with your user name or password"}), 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return jsonify({"type":"Error" ,"message:": "Database does not exist"}), 404
        else:
            print(err)
            return err


def create_watchlist(user_id,name,Is_main):
    # Query to get the last inserted id for the given user_id
    watchlist_id_query = "SELECT ID FROM `final_project_db`.`watch_lists_names` WHERE User_ID = %s ORDER BY ID DESC LIMIT 1"
    try:
     if (Is_main):
         query = f"SELECT EXISTS(SELECT 1 FROM `final_project_db`.`watch_lists_names` WHERE User_ID = %s AND Main= %s)"
         cursor.execute(query, (user_id,True))
         exists = cursor.fetchone()[0]
         if not exists:
             # Insert the ID if it does not exist
             insert_query = "INSERT INTO `final_project_db`.`watch_lists_names` (User_ID, name, Main) VALUES (%s, %s, %s)"
             cursor.execute(insert_query, (user_id,'Main',True ))
             print(type(user_id))
             connection.commit()
             print(f"ID {user_id}  list was added to the table .")
             cursor2.execute(watchlist_id_query, (user_id,))
             main_watchlist_id = cursor2.fetchall()[0]
             print (main_watchlist_id)
             return main_watchlist_id
         else:
             print(f"ID {user_id}  list main watchlist already exists in the table .")
             return f"ID {user_id}  list main watchlist already exists in the table .", 201
     else :
         insert_query = f"INSERT INTO `final_project_db`.`watch_lists_names` (User_ID,name,Main) VALUES (%s,%s,%s)"
         cursor.execute(insert_query, (user_id, name, False))
         connection.commit()
         cursor2.execute(watchlist_id_query, (user_id,))

         new_id = cursor2.fetchall()[0]
         return new_id
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

def remove_watch_list(userID,watch_list_id):
    try:
        # Delete watchlist object, not items
        delete_query1 = "DELETE FROM `final_project_db`.`watch_lists_names` WHERE `ID`= %s AND `User_ID`= %s ;"
        cursor.execute(delete_query1, (watch_list_id, userID))
        connection.commit()
        if cursor.rowcount > 0:
            # Delete items from watchlist
            delete_query2 = "DELETE FROM `final_project_db`.`watch_lists_objects` WHERE `Parent_ID`= %s AND `User_ID`= %s ;"
            cursor.execute(delete_query2, (watch_list_id, userID))
            connection.commit()
            print(f"Deletion of watchlist {watch_list_id} successful")
            return jsonify({"type": "success", "message": f"Removed watchlist {watch_list_id}"}), 200
        else:
            return jsonify({"type": "Failure", "message": "No watchlist deleted. Please make sure it belongs to the logged in user"}), 200
        # Delete items from watchlist
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return jsonify({"type":"Error" , "message:": "Something is wrong with your user name or password"}), 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return jsonify({"type":"Error" ,"message:": "Database does not exist"}), 404
        else:
            print(err)
            return err
			
def get_user_watchlists(user_id):
    try:
         query = f"SELECT * FROM `final_project_db`.`watch_lists_names` WHERE User_ID = %s"
         cursor2.execute(query, (user_id,))
         return cursor2.fetchall()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return jsonify({"type":"Error" ,"message":"Something is wrong with your user name or password"}), 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return jsonify({"type":"Error" ,"message":"Database does not exist"}), 404
        else:
            print(err)
            return err


def get_watchlist_by_id(watchlist_ID):
    try:

        query = f"SELECT * FROM `final_project_db`.`watch_lists_objects` WHERE Parent_ID = %s"
        cursor2.execute(query, (watchlist_ID,))
        results = cursor2.fetchall()
        return results

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return jsonify({"type":"Error" ,"message":"Something is wrong with your user name or password"}), 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return jsonify({"type":"Error" ,"message":"Database does not exist"}), 404
        else:
            print(err)
            return err


def get_watchlist_details_only(watchlist_ID):
    try:
        query = f"SELECT * FROM `final_project_db`.`watch_lists_names` WHERE ID = %s"
        cursor2.execute(query, (watchlist_ID,))
        results = cursor2.fetchall()
        print("watchlist deets " , results, "watchlist id " , watchlist_ID)
        return results[0]

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return jsonify({"type":"Error" ,"message":"Something is wrong with your user name or password"}), 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return jsonify({"type":"Error" ,"message":"Database does not exist"}), 404
        else:
            print(err)
            return err


def get_main_watchlist(user_ID):
    try:

        query = f"SELECT * FROM `final_project_db`.`watch_lists_names` WHERE User_ID = %s AND Main = 1"
        cursor2.execute(query, (user_ID,))
        results = cursor2.fetchall()
        return results

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return jsonify({"type":"Error" ,"message":"Something is wrong with your user name or password"}), 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return jsonify({"type":"Error" ,"message":"Database does not exist"}), 404
        else:
            print(err)
            return err
