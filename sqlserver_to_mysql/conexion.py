import mysql.connector
from mysql.connector import Error
import pyodbc
from dataclasses import dataclass

@dataclass
class Conexiones:
    mydb=None
    serverdb=None

    def crear_base_datos(self):
        try:
            if self.mydb.is_connected():
                    mycursor = self.mydb.cursor()
                    mycursor.execute("DROP DATABASE IF EXISTS BibliotecaUniversidad;")
                    mycursor.execute("CREATE DATABASE IF NOT EXISTS BibliotecaUniversidad;")
                    mycursor.execute("USE BibliotecaUniversidad;")
                    mycursor.close()
        except:
            print("Data base creation error")

    def conectar_mysql(self):
        try:
            self.mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    port='3306',
                    password='Fernando2420'
            )
            self.crear_base_datos()
        except Error:
            print(f"Connection error in mysql")
        

    def conectar_sqlserver(self):
        server = 'DESKTOP-T8BJL71'  
        database = 'BibliotecaUniversitaria'
        username = 'DESKTOP-T8BJL71\\user'

        try:
            self.serverdb = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={username};"
                f"Trusted_Connection=yes;"
            )
        except:
            print('Connection error in sqlserver')
    
    def cerrar_conexiones(self):
        self.mydb.close()
        self.serverdb.close()
