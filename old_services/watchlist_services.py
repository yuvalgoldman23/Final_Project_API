from database_connector import connection, cursor, cursor2
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify




def add_watch_list_item(userID,Media_TMDB_ID,Parent_ID, is_movie):
    try:
        sql_check_query = "SELECT * FROM `final_project_db`.`watch_lists_objects` WHERE User_ID=%s and  TMDB_ID=%s and Parent_ID=%s"
        #check_tuple = (post_id, tagged_media_id, start_position, length)
        cursor.execute(sql_check_query, (userID,Media_TMDB_ID,Parent_ID))
        result = cursor.fetchone()

        if result:
            # Tag already exists, return its ID
            return "The media alredy in the list", 200
        else:
         insert_query = f"INSERT INTO `final_project_db`.`watch_lists_objects`(`User_ID`,`TMDB_ID`,`Parent_ID`, `is_movie`) VALUES (%s,%s,%s, %s) "
         cursor.execute(insert_query, (userID,Media_TMDB_ID ,Parent_ID, is_movie))
         connection.commit()
         return "Added movie {} to watchlist {}".format(Media_TMDB_ID, Parent_ID)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return jsonify({"type":"Error" , "message:": "Something is wrong with your user name or password"})
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return jsonify({ "type":"Error" ,"message:": "Database does not exist"})
        else:
            print(err)
            return err



def remove_watch_list_item(userID,watch_list_item_id):
    try:
        delete_query = "DELETE FROM `final_project_db`.`watch_lists_objects` WHERE `ID`= %s AND `User_ID`= %s ;"
        cursor.execute(delete_query, (watch_list_item_id, userID))
        connection.commit()
        if cursor.rowcount > 0:
            print(f"Deletion of watchlist item {watch_list_item_id} successful")
            return jsonify({"type": "success", "message": f"Removed item {watch_list_item_id}"}), 200
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
    watchlist_id_query = "SELECT id  FROM `final_project_db`.`watch_lists_names` WHERE User_ID = %s and  name=%s "


    try:
     if (Is_main):
         query = f"SELECT EXISTS(SELECT 1 FROM `final_project_db`.`watch_lists_names` WHERE User_ID = %s AND Main= %s)"
         cursor.execute(query, (user_id,True))
         exists = cursor.fetchone()[0]
         if not exists:
             # Insert the ID if it does not exist
             insert_query = f"INSERT INTO `final_project_db`.`watch_lists_names` User_ID,name,Main) VALUES (%s,%s,%s)"
             cursor.execute(insert_query, (user_id,"Main",True ))
             connection.commit()
             print(f"ID {user_id}  list was added to the table .")
             cursor2.execute(watchlist_id_query, (user_id,name))
             return cursor2.fetchall()
         else:
             print(f"ID {user_id}  list main watchlist already exists in the table .")
             cursor2.execute(watchlist_id_query, (user_id, name))
             return cursor2.fetchall()
     else :
         query = f"SELECT ID FROM `final_project_db`.`watch_lists_names` WHERE User_ID = %s AND name= %s"
         cursor.execute(query, (user_id, True))
         exists = cursor.fetchone()
         if not exists:
          insert_query = f"INSERT INTO `final_project_db`.`watch_lists_names` (User_ID,name,Main) VALUES (%s,%s,%s)"
          cursor.execute(insert_query, (user_id, name, False))
          connection.commit()
          cursor2.execute(watchlist_id_query, (user_id,))
          new_id = cursor2.fetchall()
          return new_id
         else:
             cursor2.execute(watchlist_id_query, (user_id,))
             new_id = cursor2.fetchall()
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

