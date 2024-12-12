from tkinter import Tk
from biblioteca_app import BibliotecaApp
from db_conexion import DatabaseConnection
import sys
import os
# Añadir archivo de migracion
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sqlserver_to_mysql')))
from migration_main import *

config = {
    "db_type": "mysql",  #Cambio de db en la interfaz
    "connection_params": {
        "host": "localhost",
        "user": "root",
        "password": "Fernando2420",#Fernando: Fernando2420
        "database": "BibliotecaUniversidad",
        "auth_plugin":'mysql_native_password'
    }
}

if __name__=="__main__":
    root=Tk()
    db_connection=DatabaseConnection(config["db_type"], config["connection_params"])
    app=BibliotecaApp(root, db_connection)
    root.mainloop()
