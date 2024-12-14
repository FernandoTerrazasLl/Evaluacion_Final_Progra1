from tkinter import Tk
from biblioteca_app import BibliotecaApp
import sys
import os

# Configurar el acceso al módulo de migración
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sqlserver_to_mysql')))
from conexion import Conexiones
from migration_main import migration_main

if __name__=="__main__":
    try:
        conexion_db=Conexiones()
        conexion_db.conectar_mysql()
        if not conexion_db.mydb or not conexion_db.mydb.is_connected():
            raise Exception("Conexión a MySQL no establecida.")
        conexion_db.conectar_sqlserver() 
    except Exception as e:
        print(f"Error al conectar a las bases de datos: {str(e)}")
        exit(1)

    try:
        conexion_db.crear_base_datos()  

        migration_main(conexion_db)
    except Exception as e:
        print(f"Error durante la creación de la base de datos o la migración: {str(e)}")
        conexion_db.cerrar_conexiones()
        exit(1)

    try:
        root=Tk()
        app=BibliotecaApp(root, conexion_db)
        root.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación Tkinter: {str(e)}")
    finally:
        conexion_db.cerrar_conexiones()