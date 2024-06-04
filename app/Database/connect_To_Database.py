import mysql.connector
from mysql.connector import errorcode
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="password",
    database="final_project_db"
)

# Check if connection is successful
if connection.is_connected():
    print("Connected to MySQL database")
    cursor = connection.cursor()

def addmsg(msg):
    query="INSERT INTO `final_project_db`.`messages`(`message_text`) VALUES (%s);"
    data=(msg,)
    cursor.execute(query,data)
    connection.commit()


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
                return(f"ID {id}'s, email {email} registration has been successfully completed.")
            else:
                return(f"ID {id}, email {email} is already registered.")

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)



def Write_review_or_comment(Writer_ID,media_ID,TEXT,IsReview):
       try:
           insert_query = f"INSERT INTO `final_project_db`.`reviews`(`Writer_ID`,`TText`,`IsReview`,`Parent_ID`) VALUES (%s,%s,%s,%s) "
           cursor.execute(insert_query, (Writer_ID, TEXT, IsReview, media_ID))
           connection.commit()
       except mysql.connector.Error as err:
           if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
               print("Something is wrong with your user name or password")
           elif err.errno == errorcode.ER_BAD_DB_ERROR:
               print("Database does not exist")
           else:
               print(err)



def Update_Text(Review_ID,Writed_ID,TEXT):
    try:
        update_query = "UPDATE FROM `final_project_db`.`watch_list` SET `TText`=%s WHERE `ID`= %s AND `Writer_ID`= %s ;"
        cursor.execute(update_query, (TEXT, Review_ID, Writed_ID))
        connection.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

def Remove_Review (Review_ID,Writed_ID):
     try:
          delete_query="DELETE FROM `final_project_db`.`reviews` WHERE `ID`= %s AND `Writer_ID`= %s ;"
          cursor.execute(delete_query, (Review_ID,Writed_ID))
          connection.commit()
     except mysql.connector.Error as err:
         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
             print("Something is wrong with your user name or password")
         elif err.errno == errorcode.ER_BAD_DB_ERROR:
             print("Database does not exist")
         else:
             print(err)


def add_watch_list_item(userID,Media_TMDB_ID,Is_movie,Comment,Is_watched,Rating,Progress):
    try:
        insert_query = f"INSERT INTO `final_project_db`.`watch_list`(`Owner_ID`,`Media_ID`,`Is_Movie`,`Comment`,`Watched`,`Rating`,`progress`) VALUES (%s,%s,%s,%s,%s,%s,%s) "
        cursor.execute(insert_query, (userID,Media_TMDB_ID ,Is_movie, Comment,Is_watched,Rating,Progress))
        connection.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

def remove_watch_list_item(userID,watch_list_item_id):
    try:
        delete_query = "DELETE FROM `final_project_db`.`reviews` WHERE `ID`= %s AND `Writer_ID`= %s ;"
        cursor.execute(delete_query, (watch_list_item_id, userID))
        connection.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
def update_Watched_status(Watch_item_id,user_id,Watched_value):
    try:
        update_query = "UPDATE FROM `final_project_db`.`watch_list` SET `Prpgress`=%s WHERE `ID`= %s AND `Owner_ID`= %s ;"
        cursor.execute(update_query, (Watched_value,Watch_item_id,user_id))
        connection.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
def update_Rating (Watch_item_id,user_id,Rating):

        try:
            update_query = "UPDATE FROM `final_project_db`.`watch_list` SET `Rating`=%s WHERE `ID`= %s AND `Owner_ID`= %s ;"
            cursor.execute(update_query, (Rating, Watch_item_id, user_id))
            connection.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        t=6
def upsate_Comment (Watch_item_id,user_id,Comment):
    try:
        update_query = "UPDATE FROM `final_project_db`.`watch_list` SET `Comment`=%s WHERE `ID`= %s AND `Owner_ID`= %s ;"
        cursor.execute(update_query, (Comment, Watch_item_id, user_id))
        connection.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    t = 6
    t=5
def update_Progress (Watch_item_id,user_id,Progress):
    try:
        update_query = "UPDATE FROM `final_project_db`.`watch_list` SET `Progress`=%s WHERE `ID`= %s AND `Owner_ID`= %s ;"
        cursor.execute(update_query, (Progress, Watch_item_id, user_id))
        connection.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    t = 6





