from database_connector import connection, cursor, cursor2
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify


def Add_rating(User_ID, Media_id, rating, is_movie):
    # Query to check if a rating already exists for the given user and media
    check_existing_query = "SELECT ID FROM `final_project_db`.`rating` WHERE User_ID = %s AND Media_ID = %s AND is_movie = %s LIMIT 1"

    try:
        cursor.execute(check_existing_query, (User_ID, Media_id, is_movie))
        existing_rating = cursor.fetchall()

        if existing_rating:
            print(update_rating(Media_id, is_movie, User_ID, rating))
            return "success updated rating", 201

        # If no rating exists, proceed to insert the new rating
        insert_query = "INSERT INTO `final_project_db`.`rating`(`User_ID`,`Media_ID`,`rating`, `is_movie`) VALUES (%s,%s,%s,%s)"
        cursor.execute(insert_query, (User_ID, Media_id, rating, is_movie))
        connection.commit()

        # Get the ID of the newly inserted rating
        rating_id_query = "SELECT ID FROM `final_project_db`.`rating` WHERE User_ID = %s ORDER BY ID DESC LIMIT 1"
        cursor.execute(rating_id_query, (User_ID,))
        rating_id = cursor.fetchall()

        if rating_id:
            print(f"Successfully added rating for {Media_id}")
            return rating_id[0][0], 201  # 201 Created; Extract first element from tuple
        else:
            return "Failed to retrieve the rating ID", 500

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return "Something is wrong with your user name or password", 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return "Database does not exist", 404
        else:
            print(err)
            return str(err), 404  # Convert error to string before returning


def get_rating_of_user(user_id, content_id, is_movie):
    try:
        if content_id:
            query = "SELECT * FROM `final_project_db`.`rating` WHERE User_ID = %s AND media_ID = %s AND is_movie = %s"
            cursor2.execute(query, (user_id, content_id, is_movie))
            result = cursor2.fetchall()
            if result:
                return result[0], 200  # Return the first result
            else:
                return "No rating found for the provided content_id and user_id", 404
        else:
            query = "SELECT * FROM `final_project_db`.`rating` WHERE User_ID = %s"
            cursor2.execute(query, (user_id,))
            results = cursor2.fetchall()
            if results:
                return results, 200
            else:
                return "No ratings found for the provided user_id", 404

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return "Something is wrong with your user name or password", 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return "Database does not exist", 404
        else:
            print(err)
            return str(err), 404  # Convert error to string before returning


def Remove_rating(content_id, is_movie, User_ID):
    try:
        delete_query = "DELETE FROM `final_project_db`.`rating` WHERE `media_ID`= %s AND is_movie = %s AND `User_ID`= %s;"
        cursor.execute(delete_query, (content_id, is_movie, User_ID))
        connection.commit()
        if cursor.rowcount > 0:
            return f"Successfully removed {content_id}", 200
        else:
            return "No ratings found for such content_id and user_id", 404
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return "Something is wrong with your user name or password", 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return "Database does not exist", 404
        else:
            print(err)
            return str(err), 404  # Convert error to string before returning


def update_rating(content_id, is_movie, User_ID, new_rating):
    try:
        # Step 1: Check the current rating
        select_query = "SELECT `rating` FROM `final_project_db`.`rating` WHERE `media_ID`= %s AND is_movie = %s AND `User_ID`= %s;"
        cursor.execute(select_query, (content_id, is_movie, User_ID))
        current_rating = cursor.fetchall()

        if not current_rating:
            return "No ratings found for the provided content_id and user_id", 404

        # Step 2: Determine if the new rating is the same as the current rating
        if current_rating[0][0] == new_rating:
            return "The provided rating is the same as the current rating", 304  # 304 Not Modified

        # Step 3: Proceed with the update
        update_query = "UPDATE `final_project_db`.`rating` SET `rating` = %s WHERE `media_ID`= %s AND is_movie = %s AND `User_ID`= %s;"
        cursor.execute(update_query, (new_rating, content_id, is_movie, User_ID))
        connection.commit()

        if cursor.rowcount > 0:
            return f"Successfully updated {content_id}", 200
        else:
            return "No ratings found for such content_id and user_id", 404

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            return "Something is wrong with your user name or password", 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            return "Database does not exist", 404
        else:
            return str(err), 404  # Convert error to string before returning
