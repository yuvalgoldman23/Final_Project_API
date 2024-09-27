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
    cursor2 = connection.cursor(dictionary=True)


def handle_mysql_error(err):
    """Handle MySQL errors."""
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
