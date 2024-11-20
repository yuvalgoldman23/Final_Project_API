#from database_connector import connection, cursor, cursor2
from database_connector import connection_pool,semaphore
import mysql.connector
from mysql.connector import errorcode
from flask import jsonify , session
from routes import recommendation_routes as rr
from services import  watchlist_services as service


def login_google(id,email):
        try:
            connection2 = connection_pool.get_connection()

            cursor = connection2.cursor()
            cursor2 = connection2.cursor(dictionary=True)
            # Check if the ID exists
            query = f"SELECT EXISTS(SELECT 1 FROM `final_project_db`.`users` WHERE id = %s)"
            cursor.execute(query, (id,))
            exists = cursor.fetchall()[0][0]

            if not exists:
                # Registration: Insert the ID if it does not exist
                # Add a default region
                # TODO should the client ask upon registration?
                default_region = "US"
                insert_query = f"INSERT INTO `final_project_db`.`users` (id,username,password,email,google_auth, region) VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(insert_query, (id,email.split("@")[0],id,email,1, default_region))
                connection2.commit()
                print(f"ID {id} was added to the table .")
                main_watchlist_id = service.create_watchlist(id, "Main", True)

                ''''
                if usr==id:
                  if not (session.get('usr_pref', None)):
                      x,rr.get_usr_prep(id)
                      session['usr_pref'] = x

                else:
                    session['usr']=id
                    x = rr.get_usr_prep(id)
                    session['usr_pref'] = x
                '''
                return main_watchlist_id, 200
            else:
                print(f"ID {id} already exists in the table .")
                try:
                    main_watchlist_id = service.get_main_watchlist(id)[0].get('ID')

                    return main_watchlist_id, 200
                except TypeError:
                    return "Couldn't find main watchlist due to a DB error", 400


        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
                return "Wrong credentials", 404
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                return "Database does not exist", 404
            else:
                print("unknown error", err)
                return str(err), 404
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'cursor2' in locals() and cursor2:
                cursor2.close()
            if 'connection2' in locals() and not (connection2 is None):
                if connection2 and connection2.is_connected():
                    connection2.close()



def get_user_region_db(user_id):
    try:
        connection2 = connection_pool.get_connection()

        cursor = connection2.cursor()
        cursor2 = connection2.cursor(dictionary=True)
        query =  f"SELECT region from `final_project_db`.`users` WHERE id = %s"
        cursor.execute(query, (user_id,))
        region = cursor.fetchall()[0][0]
        return region, 200
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return "Wrong credentials", 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return "Database does not exist", 404
        else:
            print("unknown error", err)
            return str(err), 404
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'cursor2' in locals() and cursor2:
            cursor2.close()
        if 'connection2' in locals() and not (connection2 is None):
            if connection2 and connection2.is_connected():
                connection2.close()

def update_user_region(user_id,region):
    try:
        connection2 = connection_pool.get_connection()

        cursor = connection2.cursor()
        cursor2 = connection2.cursor(dictionary=True)
        query = f"UPDATE `final_project_db`.`users` SET region = %s WHERE id = %s"
        cursor.execute(query, (region, user_id))
        connection2.commit()
        print(f"ID {user_id} was updated to the table .")
        return 200
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return "Wrong credentials", 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return "Database does not exist", 404
        else:
            print("unknown error", err)
            return str(err), 404
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'cursor2' in locals() and cursor2:
            cursor2.close()
        if 'connection2' in locals() and not (connection2 is None):
            if connection2 and connection2.is_connected():
                connection2.close()


def get_user_details(id):
    try:
        connection2 = connection_pool.get_connection()

        cursor = connection2.cursor()
        cursor2 = connection2.cursor(dictionary=True)
        query = f"SELECT EXISTS(SELECT 1 FROM `final_project_db`.`users` WHERE id = %s)"
        cursor.execute(query, (id,))
        exists = cursor.fetchall[0][0]
        if exists:
         query = f"SELECT * FROM `final_project_db`.`users` WHERE id = %s"
         cursor2.execute(query, (id,))
         return cursor2.fetchall()[0],200
        else:
            return "user does not exist",404
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return "Database does not exist", 404
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return "Database does not exist", 404
        else:
            print(err)
            return err, 404
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'cursor2' in locals() and cursor2:
            cursor2.close()
        if 'connection2' in locals() and not (connection2 is None):
            if connection2 and connection2.is_connected():
                connection2.close()

