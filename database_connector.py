import mysql.connector
from mysql.connector import pooling
from mysql.connector import errorcode
import threading

connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=20,
    host="127.0.0.1",
    pool_reset_session=True,
    user="root",
    password="yanovsky",
    database="final_project_db",


)

semaphore = threading.Semaphore(10)
global_lock = threading.Lock()

# Check if connection is successful

print("Connected to MySQL database")

def handle_mysql_error(err):
    """Handle MySQL errors."""
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
