from database_connector import connection, cursor, cursor2
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify


def Add_rating(User_ID, Media_id, rating, is_movie):



    try:
        query = f"SELECT EXISTS(SELECT 1 FROM `final_project_db`.`rating` WHERE User_ID = %s AND Media_ID = %s )"
        cursor.execute(query, (User_ID,Media_id))
        exists = cursor.fetchone()[0]
        if exists:
            update_query=f"UPDATE`final_project_db`.`rating` SET rating = %s WHERE User_ID = %s AND Media_ID = %s "
            cursor.execute(update_query, (rating, User_ID, Media_id))
            connection.commit()
            return f"success updating rating for {Media_id}", 200
        else :
            insert_query = f"INSERT INTO `final_project_db`.`rating`(`User_ID`,`Media_ID`,`rating`, `is_movie`) VALUES (%s,%s,%s,%s) "
            cursor.execute(insert_query, (User_ID, Media_id, rating, is_movie))
            connection.commit()
            return f"success adding rating for {Media_id}", 200


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

def get_rating_of_user_of_movie(user_id,media_id):
    try:

         query = f"SELECT * FROM `final_project_db`.`rating` WHERE User_ID = %s AND  Media_ID = %s"
         cursor2.execute(query, (user_id,media_id))
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

def get_rating_of_user(user_id):

    try:

         query = f"SELECT * FROM `final_project_db`.`rating` WHERE User_ID = %s"
         cursor2.execute(query, (user_id,))
         return jsonify(cursor2.fetchall()),200

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return jsonify({"Something is wrong with your user name or password"}), 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return jsonify({"Database does not exist"}), 404


        else:
            print(err)
            return err,404


def Remove_rating(rating_object_ID, User_ID):
    try:
        delete_query = "DELETE FROM `final_project_db`.`reviews` WHERE `ID`= %s AND `User_ID`= %s ;"
        cursor.execute(delete_query, (rating_object_ID, User_ID))
        connection.commit()
        return jsonify({"succses"}), 200
    except mysql.connector.Error as err:

        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:

            print("Something is wrong with your user name or password")
            return jsonify({"Something is wrong with your user name or password"}), 404

        elif err.errno == errorcode.ER_BAD_DB_ERROR:

            print("Database does not exist")
            return jsonify({"Database does not exist"}), 404

        else:
            print(err)
            return err,404
