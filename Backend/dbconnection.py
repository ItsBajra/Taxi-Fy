# import sys

# import mysql.connector


# def Connect():
#     conn = None
#     try:
#         conn = mysql.connector.Connect(
#             host='localhost',
#             username='root',
#             password='9813443979',
#             database='Assignment2'
#         )

#     except:
#         print('Error', sys.exc_info())

#     finally:
#         return conn

import sys
import mysql.connector

def Connect():
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # Use 'user' instead of 'username'
            password='9813443979',
            database='Assignment2'
        )
        print("Connected successfully!")
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print("Error:", err)
    except:
        print('Error:', sys.exc_info())
    finally:
        return conn

# Test the connection
connection = Connect()
