# EJECUTAR ESTE CODIGO PARA HACER LA MIGRACION CORRESPONDIENTE
from conexion import Conexiones
from migration_main import migration_main

if __name__=="__main__":
    try:
        print("Iniciando migración de datos...")

        # Crear conexión a bases de datos
        conexion_db=Conexiones()
        conexion_db.conectar_mysql()  # Conexión a MySQL
        conexion_db.conectar_sqlserver()  # Conexión a SQL Server
        
        # Ejecutar la migración
        migration_main(conexion_db)

        print("Migración completada exitosamente.")
    except Exception as e:
        print(f"Error durante la migración: {str(e)}")
    finally:
        # Cerrar conexiones
        conexion_db.cerrar_conexiones()
        print("Conexiones cerradas.")