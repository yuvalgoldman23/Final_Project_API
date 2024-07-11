import mysql.connector

#Returns true if the response is an error, false otherwise
def is_db_response_error(response):
    if isinstance(response, mysql.connector.Error):
        return True
    else:
        return False

def isNegative(num):
    if num < 0:
        return True
    else:
        return False
