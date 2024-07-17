from database_connector import connection, cursor, cursor2
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify


def Add_rating(User_ID, Media_id, rating, is_movie):
    # Query to get the last inserted id for the given user_id
    rating_id_query = "SELECT ID FROM `final_project_db`.`rating` WHERE User_ID = %s ORDER BY ID DESC LIMIT 1"
    try:
        insert_query = f"INSERT INTO `final_project_db`.`rating`(`User_ID`,`Media_ID`,`rating`, `is_movie`) VALUES (%s,%s,%s,%s) "
        cursor.execute(insert_query, (User_ID, Media_id, rating, is_movie))
        connection.commit()
        cursor.execute(rating_id_query, (User_ID,))
        rating_id = cursor.fetchone()[0]
        print(f"success adding rating for {Media_id}")
        return rating_id, 200
    except mysql.connector.Error as err:

        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:

            print("Something is wrong with your user name or password")
            return "Something is wrong with your user name or password", 404

        elif err.errno == errorcode.ER_BAD_DB_ERROR:

            print("Database does not exist")
            return "Database does not exist", 404

        else:
            print(err)
            return err,404


def get_rating_of_user(user_id):

    try:

         query = f"SELECT * FROM `final_project_db`.`rating` WHERE User_ID = %s"
         cursor2.execute(query, (user_id,))
         return cursor2.fetchall(),200

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return "Something is wrong with your user name or password", 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return "Database does not exist", 404


        else:
            print(err)
            return err,404


def Remove_rating(rating_object_ID, User_ID):
    try:
        delete_query = "DELETE FROM `final_project_db`.`rating` WHERE `ID`= %s AND `User_ID`= %s ;"
        cursor.execute(delete_query, (rating_object_ID, User_ID))
        connection.commit()
        if cursor.rowcount > 0:
            return f"successfully removed {rating_object_ID}", 200
        else:
            return "no ratings found for such rating_id and user_id", 404
    except mysql.connector.Error as err:

        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:

            print("Something is wrong with your user name or password")
            return "Something is wrong with your user name or password", 404

        elif err.errno == errorcode.ER_BAD_DB_ERROR:

            print("Database does not exist")
            return "Database does not exist", 404

        else:
            print(err)
            return err,404
