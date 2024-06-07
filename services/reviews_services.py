from database_connector import connection, cursor, cursor2
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify


def get_reviews_of_user(user_id):
    try:

        query = f"SELECT * FROM `final_project_db`.`revies` WHERE Writer_ID = %s"
        cursor2.execute(query, (user_id,))
        return jsonify(cursor2.fetchall())

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def Write_review_or_comment(Writer_ID, Parent_ID, TEXT, IsReview):
    try:
        insert_query = f"INSERT INTO `final_project_db`.`reviews`(`Writer_ID`,`TText`,`IsReview`,`Parent_ID`) VALUES (%s,%s,%s,%s) "
        cursor.execute(insert_query, (Writer_ID, TEXT, IsReview, Parent_ID))
        connection.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def update_text(review_id, writer_id, text):
    try:
        update_query = "UPDATE FROM `final_project_db`.`watch_list` SET `TText`=%s WHERE `ID`= %s AND `Writer_ID`= %s ;"
        cursor.execute(update_query, (text, review_id, writer_id))
        connection.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def remove_review(review_id, writer_id):
    try:
        delete_query = "DELETE FROM `final_project_db`.`reviews` WHERE `ID`= %s AND `Writer_ID`= %s ;"
        cursor.execute(delete_query, (review_id, writer_id))
        connection.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
