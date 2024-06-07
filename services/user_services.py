from database_connector import connection, cursor, cursor2
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify

def login_google(user_id, email):
    try:
        # Connect to the MySQL database

        # Check if the ID exists
        query = f"SELECT EXISTS(SELECT 1 FROM `final_project_db`.`users` WHERE id = %s)"
        cursor.execute(query, (user_id,))
        exists = cursor.fetchone()[0]

        if not exists:
            # Insert the ID if it does not exist
            insert_query = f"INSERT INTO `final_project_db`.`users` (id,username,password,email,google_auth) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(insert_query, (user_id, email.split("@")[0], user_id, email, 1))
            connection.commit()
            return f"ID {user_id}'s, email {email} registration has been successfully completed."
        else:
            return f"ID {user_id}, email {email} is already registered."

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def get_user_details(user_id):
    try:
        query = f"SELECT EXISTS(SELECT 1 FROM `final_project_db`.`users` WHERE id = %s)"
        cursor.execute(query, (user_id,))
        exists = cursor.fetchone()[0]
        if exists:
            query = f"SELECT * FROM `final_project_db`.`users` WHERE id = %s"
            cursor2.execute(query, (user_id,))
            return jsonify(cursor2.fetchall()[0])
        else:
            return None

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
