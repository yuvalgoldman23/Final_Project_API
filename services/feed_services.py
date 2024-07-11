from database_connector import connection, cursor, cursor2
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify



def add_post(user_id, parent_id, is_child, text_content):
    try:
        sql_insert_query = """INSERT INTO posts (user_id, parent_id, is_child, text_content, created_at)
                                          VALUES (%s, %s, %s, %s, NOW())"""

        # Tuple to hold data
        insert_tuple = (user_id, parent_id, is_child, text_content)

        # Execute the query
        cursor.execute(sql_insert_query, insert_tuple)
        connection.commit()

        # Get the last inserted ID
        post_id_query = "SELECT id FROM `final_project_db`.`posts` WHERE user_id = %s ORDER BY id DESC LIMIT 1"
        cursor.execute(post_id_query, (user_id,))
        last_inserted_id = cursor.fetchone()[0]

        return last_inserted_id,200

    except mysql.connector.Error as err:
        print (err)
        return err, 404

# Returns true if 'id' is an id of a post that exists in the DB
def does_post_id_exist(id):
    try:
        query = f"SELECT * FROM `final_project_db`.`posts` WHERE id = %s "
        cursor2.execute(query, (id,))
        result = cursor2.fetchone()
        print(result)
        if result is None:
            print("No post exists")
            return False
        return True

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return False
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return False


        else:
            print(err)
            return err

def get_posts_by_parentid(parentid, number_of_posts):
    try:
        if number_of_posts:
            query = f"SELECT * FROM `final_project_db`.`posts` WHERE parent_id = %s ORDER BY created_at DESC LIMIT {number_of_posts}"
        else:
            query = f"SELECT * FROM `final_project_db`.`posts` WHERE parent_id = %s "
        cursor2.execute(query, (parentid, ))
        return cursor2.fetchall(), 200

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return "Something is wrong with your user name or password", 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return "Database does not exist", 404


        else:
            print(err)
            return err, 404


def update_post_text(postid, newtext, user_id):
    try:
        sql_update_query = "UPDATE posts SET text_content = %s WHERE id = %s AND user_id = %s"

        # Tuple to hold data
        update_tuple = (newtext, postid, user_id)
        # Execute the query
        cursor.execute(sql_update_query, update_tuple)
        connection.commit()

        # Check the number of affected rows
        if cursor.rowcount == 0:
            return "Post ID does not exist or does not belong to the provided user ID", 404

        return "success", 200
    except mysql.connector.Error as err:
        print(err)
        return str(err), 500


def get_posts_by_user(user_id, number_of_posts):
    try:
        if number_of_posts:
            query = f"SELECT * FROM `final_project_db`.`posts` WHERE user_id = %s ORDER BY created_at DESC LIMIT {number_of_posts}"
        else:
            query = f"SELECT * FROM `final_project_db`.`posts` WHERE user_id = %s "
        cursor2.execute(query, (user_id,))
        return cursor2.fetchall(), 200

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return "Something is wrong with your user name or password", 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return "Database does not exist", 404


        else:
            print(err)
            return err, 404



def get_last_n_posts(number_of_posts, timestamp=None):
    try:
        if timestamp:
            query = f"""
            SELECT * FROM `final_project_db`.`posts` 
            WHERE created_at < %s 
            ORDER BY created_at DESC 
            LIMIT %s
            """
            cursor2.execute(query, (timestamp, number_of_posts))
        else:
            query = f"""
            SELECT * FROM `final_project_db`.`posts` 
            ORDER BY created_at DESC 
            LIMIT %s
            """
            cursor2.execute(query, (number_of_posts,))

        return cursor2.fetchall(), 200

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return "Something is wrong with your user name or password", 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return "Database does not exist", 404
        else:
            print(err)
            return str(err), 500



def remove_post(post_id, user_id):
   try:
    sql_delete_query = "DELETE FROM `final_project_db`.`posts` WHERE `id` = %s AND `user_id` =%s;"

    # Execute the query
    cursor.execute(sql_delete_query, (post_id, user_id))
    connection.commit()

    # Check if the row was deleted
    if cursor.rowcount > 0:
        print("Post deleted successfully")
        return f"Successfully deleted post {post_id}", 201
    else:
        return "Post ID does not exist or does not belong to the provided user ID", 404

   except mysql.connector.Error as err:
        print(err)
        return err, 404

def add_tag(post_id, tagged_media_id, start_position, length):
    try:
        sql_insert_query = """INSERT INTO tags (post_id, tagged_media_id, start_position, length)
                                          VALUES (%s, %s, %s, %s)"""

        # Tuple to hold data
        insert_tuple = (post_id, tagged_media_id, start_position, length)

        # Execute the query
        cursor.execute(sql_insert_query, insert_tuple)
        connection.commit()

        # Get the last inserted ID
        tag_id_query = "SELECT id FROM `final_project_db`.`tags` WHERE post_id = %s ORDER BY post_id DESC LIMIT 1"
        cursor.execute(tag_id_query, (post_id,))
        last_inserted_id = cursor.fetchone()[0]

        return last_inserted_id

    except mysql.connector.Error as err:
        print(err)
        return err,404

def get_tags_of_post(postid):
    try:

        query = f"SELECT * FROM `final_project_db`.`tags` WHERE post_id = %s "
        cursor2.execute(query, (postid))
        return cursor2.fetchall(), 200

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return "Something is wrong with your user name or password", 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return "Database does not exist", 404


        else:
            print(err)
            return err, 404

def get_tags_of_media(media_id):
    try:

        query = f"SELECT post_id FROM `final_project_db`.`tags` WHERE tagged_media_id = %s "
        cursor2.execute(query, (media_id))
        return cursor2.fetchall(), 200

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return "Something is wrong with your user name or password", 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return "Database does not exist", 404


        else:
            print(err)
            return err, 404
def get_mentions_of_user(user_id):
    try:

        query = f"SELECT post_id FROM `final_project_db`.`mentions` WHERE mentioned_user_id= %s "
        cursor2.execute(query, (user_id))
        return cursor2.fetchall(), 200

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return "Something is wrong with your user name or password", 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return "Database does not exist", 404
        else:
            print(err)
            return err, 404
def get_mentions_of_post(postid):
    try:

        query = f"SELECT * FROM `final_project_db`.`mentions` WHERE post_id = %s "
        cursor2.execute(query, (postid))
        return cursor2.fetchall(), 200

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return "Something is wrong with your user name or password", 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return "Database does not exist", 404


        else:
            print(err)
            return err, 404
def remove_tag(tag_id):

    try:
        # SQL Delete Query
        sql_delete_query = """DELETE FROM tags WHERE id = %s"""

        # Execute the query
        cursor.execute(sql_delete_query, (tag_id,))
        connection.commit()

        # Check if the row was deleted
        if cursor.rowcount > 0:
            print("Tag deleted successfully")
            return "success",200
        else:
            print("Tag not found")
            return "error",404

    except mysql.connector.Error as err:
        print(err)
        return err,404


def add_mention(post_id, mentioned_user_id, start_position, length):
    try:

        # SQL Insert Query
        sql_insert_query = """INSERT INTO mentions (post_id, mentioned_user_id, start_position, length)
                                         VALUES (%s, %s, %s, %s)"""

        # Tuple to hold data
        insert_tuple = (post_id, mentioned_user_id, start_position, length)

        # Execute the query
        cursor.execute(sql_insert_query, insert_tuple)
        connection.commit()

        # Get the last inserted ID
        # Get the last inserted ID
        tag_id_query = "SELECT id FROM `final_project_db`.`mentions` WHERE post_id = %s ORDER BY post_id DESC LIMIT 1"
        cursor.execute(tag_id_query, (post_id,))
        last_inserted_id = cursor.fetchone()[0]

        return last_inserted_id

    except mysql.connector.Error as err:
        print(err)
        return None


def remove_mention(mention_id):

    try:
        sql_delete_query = """DELETE FROM mentions WHERE id = %s"""

        # Execute the query
        cursor.execute(sql_delete_query, (mention_id,))
        connection.commit()

        # Check if the row was deleted
        if cursor.rowcount > 0:
            print("Mention deleted successfully")
            return "success",200
        else:
            print("Mention not found")
            return "error",404

    except mysql.connector.Error as err:
        print(err)
        return err,404