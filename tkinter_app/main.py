from tkinter import Tk
from biblioteca_app import BibliotecaApp
import sys
import os

# Configurar el acceso al módulo de migración
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sqlserver_to_mysql')))
from conexion import Conexiones
from migration_main import migration_main

def main():
    # Establecer conexiones
    conexion_db=Conexiones()
    try:
        # Conexión a MySQL
        conexion_db.conectar_mysql(usar_base_datos=True)  # Usar directamente la base de datos migrada
        if not conexion_db.mydb or not conexion_db.mydb.is_connected():
            raise Exception("Conexión a MySQL no establecida.")

        # Conexión a SQL Server
        conexion_db.conectar_sqlserver()
    except Exception as e:
        print(f"Error al conectar a las bases de datos: {str(e)}")
        exit(1)

    # Proceso de migración
    try:
        print("Iniciando proceso de migración...")
        migration_main(conexion_db)
        print("Migración completada con éxito.")
    except Exception as e:
        print(f"Error durante la migración: {str(e)}")
        conexion_db.cerrar_conexiones()
        exit(1)

    # Iniciando la app Tkinter
    try:
        root=Tk()
        app = BibliotecaApp(root, conexion_db)  # Pasar la conexión a la aplicación
        root.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación Tkinter: {str(e)}")
    finally:
        # Cerrar conexiones al finalizar
        conexion_db.cerrar_conexiones()
        print("Conexiones cerradas correctamente.")

if __name__=="__main__":
    main()