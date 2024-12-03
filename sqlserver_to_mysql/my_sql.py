import mysql.connector
from mysql.connector import Error

try:
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            port='3306',
            password='Fernando2420'
        )

    if mydb.is_connected():
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS BibliotecaUniversidad;")
        mycursor.execute("USE BibliotecaUniversidad;")

except Error as e:
    print(f"Error: {e}")



