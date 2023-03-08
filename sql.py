import mysql.connector
from mysql.connector import Error

def create_con(hostname, username, pwd,dbname):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = hostname,
            user = username,
            password = pwd,
            database = dbname
        )
        print("Successful connection")
    except Error as e:
        print("Unsuccessful connection. The error is: ", e)
    return connection

def execute_query(conn, query):
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
        print("Successful execution")
    except Error as e:
        print("Unsuccessful execution. The error is: ", e)

def execute_read_query(conn, query):
    cursor = conn.cursor(dictionary=True)
    rows = None
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print("Unsuccessful. The error is:", e)