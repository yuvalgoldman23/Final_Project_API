import mysql.connector

connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="yanovsky",
    database="final_project_db"
)

# Check if connection is successful
if connection.is_connected():
    print("Connected to MySQL database")
    cursor = connection.cursor()
    cursor2 = connection.cursor(dictionary=True)
