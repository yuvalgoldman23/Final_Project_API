from database_connector import connection, cursor, cursor2
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify




def add_watch_list_item(userID,Media_TMDB_ID,Parent_ID):
    try:
        insert_query = f"INSERT INTO `final_project_db`.`watch_lists_objects`(`User_ID`,`TMDB_ID`,`Parent_ID`) VALUES (%s,%s,%s) "
        cursor.execute(insert_query, (userID,Media_TMDB_ID ,Parent_ID))
        connection.commit()
        return jsonify({"type":"success" ,"massage":"Complited"})
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
        return jsonify({"type":"success" ,"massage":"Complited"})
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

def remove_watch_list(userID,watch_list_id):
    try:
        delete_query1 = "DELETE FROM `final_project_db`.`watch_lists_names` WHERE `ID`= %s AND `User_ID`= %s ;"

        cursor.execute(delete_query1, (watch_list_id, userID))
        delete_query2 = "DELETE FROM `final_project_db`.`watch_lists_objects` WHERE `Parent_ID`= %s AND `User_ID`= %s ;"
        cursor.execute(delete_query2, (watch_list_id, userID))
        connection.commit()
        return jsonify({"type":"success" ,"massage":"Complited"})
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
         return jsonify(cursor2.fetchall())



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

