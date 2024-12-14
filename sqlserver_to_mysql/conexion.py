import mysql.connector
from mysql.connector import Error
import pyodbc
from dataclasses import dataclass

@dataclass
class Conexiones:
    mydb=None
    serverdb=None
    #Crea base de datos en MYSQL
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
    #ESTABLE CONEXION CON MYSQL
    def conectar_mysql(self):
        try:
            self.mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                port='3306',
                password='Fernando2420',  # Ajusta según sea necesario
                auth_plugin='mysql_native_password'
            )
            self.crear_base_datos()  # Crear la base de datos
        except mysql.connector.Error as e:
            print(f"Error al conectar a MySQL: {e}")
            self.mydb = None
    #ESTABLECE CONEXION CON SQLSERVER
    def conectar_sqlserver(self):
        server = 'DESKTOP-T8BJL71'  #Fernando: DESKTOP-T8BJL71
        database = 'BibliotecaUniversitaria'
        username = 'DESKTOP-T8BJL71/user'  #Fernando: DESKTOP-T8BJL71\user

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
    #CIERRA LAS AMBAS CONEXIONES SI AMBAS ESTAN ABIERTAS
    def cerrar_conexiones(self):
        if self.mydb and self.serverdb:
            self.mydb.close()
            self.serverdb.close()
        else:
            print("Error in docoument conexion in cerrar_conexiones, no conection")
