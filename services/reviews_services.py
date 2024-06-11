from database_connector import connection, cursor, cursor2
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify




def Write_review(User_ID,Parent_ID,TEXT):
       try:
           insert_query = f"INSERT INTO `final_project_db`.`reviews`(`User_ID`,`TText`,`Parent_ID`) VALUES (%s,%s,%s,%s) "
           cursor.execute(insert_query, (User_ID, TEXT, Parent_ID))
           connection.commit()
       except mysql.connector.Error as err:

           if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:

               print("Something is wrong with your user name or password")
               return jsonify({"Something is wrong with your user name or password"}), 404

           elif err.errno == errorcode.ER_BAD_DB_ERROR:

               print("Database does not exist")
               return jsonify({"Database does not exist"}), 404

           else:
               print(err)
               return err
			   

def get_rewies_of_user(user_id):

    try:

         query = f"SELECT * FROM `final_project_db`.`revies` WHERE User_ID = %s"
         cursor2.execute(query, (user_id,))
         return jsonify(cursor2.fetchall())




    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return jsonify({"Something is wrong with your user name or password"}), 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return jsonify({"Database does not exist"}), 404


        else:
            print(err)
            return err


def get_rewies_by_parent(parent_id):

    try:

         query = f"SELECT * FROM `final_project_db`.`revies` WHERE Parent_ID = %s"
         cursor2.execute(query, (parent_id,))
         return jsonify(cursor2.fetchall())



    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
			


def Remove_Review (Review_ID,User_ID):
     try:
          delete_query="DELETE FROM `final_project_db`.`reviews` WHERE `ID`= %s AND `User_ID`= %s ;"
          cursor.execute(delete_query, (Review_ID,User_ID))
          connection.commit()
     except mysql.connector.Error as err:

          if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:

              print("Something is wrong with your user name or password")
              return jsonify({"Something is wrong with your user name or password"}), 404

          elif err.errno == errorcode.ER_BAD_DB_ERROR:

              print("Database does not exist")
              return jsonify({"Database does not exist"}), 404

          else:
              print(err)
              return err
