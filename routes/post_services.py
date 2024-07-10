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
        last_inserted_id = cursor.lastrowid

        return last_inserted_id

    except mysql.connector.Error as err:
        print (err)
        return 404

def remove_post(post_id):
   try:
    sql_delete_query = """DELETE FROM posts WHERE id = %s"""

    # Execute the query
    cursor.execute(sql_delete_query, (post_id,))
    connection.commit()

    # Check if the row was deleted
    if cursor.rowcount > 0:
        print("Post deleted successfully")
    else:
        print("Post not found")

   except mysql.connector.Error as err:
        print(err)
        return 404

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
        last_inserted_id = cursor.lastrowid

        return last_inserted_id

    except mysql.connector.Error as err:
        print(err)
        return 404

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
            return 200
        else:
            print("Tag not found")
            return 404

    except mysql.connector.Error as err:
        print(err)
        return 404


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
        last_inserted_id = cursor.lastrowid

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
            return 200
        else:
            print("Mention not found")
            return 404

    except mysql.connector.Error as err:
        print(err)
        return 404