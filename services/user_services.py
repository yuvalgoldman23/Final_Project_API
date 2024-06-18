from database_connector import connection, cursor, cursor2
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify
from services import  watchlist_services as service


def login_google(id,email):

        try:
            # Connect to the MySQL database


            # Check if the ID exists
            query = f"SELECT EXISTS(SELECT 1 FROM `final_project_db`.`users` WHERE id = %s)"
            cursor.execute(query, (id,))
            exists = cursor.fetchone()[0]

            if not exists:
                # Insert the ID if it does not exist
                insert_query = f"INSERT INTO `final_project_db`.`users` (id,username,password,email,google_auth) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(insert_query, (id,email.split("@")[0],id,email,1))
                connection.commit()
                print(f"ID {id} was added to the table .")
                service.add_watch_list(id, "Main", True)
            else:
                print(f"ID {id} already exists in the table .")

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
                return jsonify({"Database does not exist"}), 404
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                return jsonify({"type":"Error" ,"message":"Database does not exist"}), 404
            else:
                print(err)
                return jsonify({"type":"Error" ,"message":"Database does not exist"}), 404


def get_user_details(id):
    try:
        query = f"SELECT EXISTS(SELECT 1 FROM `final_project_db`.`users` WHERE id = %s)"
        cursor.execute(query, (id,))
        exists = cursor.fetchone()[0]
        if exists:
         query = f"SELECT * FROM `final_project_db`.`users` WHERE id = %s"
         cursor2.execute(query, (id,))
         return jsonify(cursor2.fetchall()[0])
        else:
            return jsonify({"message": "Completed"})
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return jsonify({"Database does not exist"}), 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return jsonify({"type":"Error" ,"message":"Database does not exist"}), 404
        else:
            print(err)
            return jsonify({"type":"Error" ,"message":"Database does not exist"}), 404

