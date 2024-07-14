from database_connector import connection, cursor, cursor2
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify




def write_review(User_ID, Parent_ID, TEXT):
       review_id_query = "SELECT ID FROM `final_project_db`.`reviews` WHERE User_ID = %s ORDER BY ID DESC LIMIT 1"
       try:
           insert_query = f"INSERT INTO `final_project_db`.`reviews`(`User_ID`,`Text`,`Parent_ID`) VALUES (%s,%s,%s) "
           cursor.execute(insert_query, (User_ID, TEXT, Parent_ID))
           connection.commit()
           cursor2.execute(review_id_query, (User_ID,))
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
               return err, 404
			   

def get_reviews_by_user(user_id):

    try:

         query = f"SELECT * FROM `final_project_db`.`reviews` WHERE User_ID = %s"
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
            return err


def get_reviews_by_content(parent_id):

    try:

         query = f"SELECT * FROM `final_project_db`.`reviews` WHERE Parent_ID = %s"
         cursor2.execute(query, (parent_id,))
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
			


def Remove_Review (Review_ID,User_ID):
     try:
          delete_query="DELETE FROM `final_project_db`.`reviews` WHERE `ID`= %s AND `User_ID`= %s ;"
          cursor.execute(delete_query, (Review_ID,User_ID))
          connection.commit()
          if cursor.rowcount > 0:
              return "successfully deleted", 200
          else:
              return "no reviews found for such review_id and user_id", 404
     except mysql.connector.Error as err:

          if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:

              print("Something is wrong with your user name or password")
              return "Something is wrong with your user name or password", 404

          elif err.errno == errorcode.ER_BAD_DB_ERROR:

              print("Database does not exist")
              return "Database does not exist", 404

          else:
              print(err)
              return err, 400
