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
        select_quert="select ID from post where user_id = %s and parent_id= %s"
        cursor2.execute(select_quert, insert_tuple)

        return cursor2.fetchall(),200

    except mysql.connector.Error as err:
        print (err)
        return err, 404

def get_post_by_parentid(parentid):
    try:

        query = f"SELECT * FROM `final_project_db`.`posts` WHERE parent_id = %s "
        cursor2.execute(query, (parentid))
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


def update_post_text(postid,newtext):
    try:
        sql_update_query = "UPDATE posts SET text_content = %s WHERE id = %s"

        # Tuple to hold data
        update_tuple = (newtext, postid)

        # Execute the query
        cursor.execute(sql_update_query, update_tuple)
        connection.commit()
       # last_inserted_id = cursor.lastrowid

        return "success",200
    except mysql.connector.Error as err:
        print(err)
        return err, 404


def get_post_by_user(user_id):
    try:

        query = f"SELECT * FROM `final_project_db`.`posts` WHERE user_id = %s "
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
        sql_select_query="SELECT id FROM taqs where post_id= %s and tagged_media_id= %s and start_position= %s and length= %s"
        cursor2.execute(sql_select_query,  insert_tuple)

        return cursor2.fetchall(),200

    except mysql.connector.Error as err:
        print(err)
        return err,404

def get_tags_of_post(postid):
    try:

        query = f"SELECT * FROM `final_project_db`.`tags` WHERE post_id = %s "
        cursor2.execute(query, (postid,))
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
        cursor2.execute(query, (media_id,))
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
def get_mentions_of_post(postid):
    try:

        query = f"SELECT * FROM `final_project_db`.`mentions` WHERE post_id = %s "
        cursor2.execute(query, (postid,))
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

        sql_select_query = "SELECT id FROM mentions where post_id= %s and mentioned_user_id= %s and start_position= %s and length= %s"
        cursor2.execute(sql_select_query, insert_tuple)

        return cursor2.fetchall(), 200

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