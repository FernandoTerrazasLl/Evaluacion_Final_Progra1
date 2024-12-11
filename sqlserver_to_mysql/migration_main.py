from conexion import Conexiones
from pruebas import Pruebas
from extraccion_datos import obtener_tablas,extraer_columnas,extraer_numero_registros,extraer_info,extraer_tipo_datos
from insertar_datos import insertar_tabla,insertar_info

conexion_db=Conexiones()
conexion_db.conectar_mysql()
conexion_db.conectar_sqlserver()
#CREANDO CURSORES PARA CONSULTAS
mycursor=conexion_db.mydb.cursor()
cursor_server=conexion_db.serverdb.cursor()

#NOMBRE TABLAS
tablas_nombres=obtener_tablas(cursor_server,"sqlserver")
try:
    for tabla in tablas_nombres:
        #FILAS INFO DE LA TABLA SQLSERVER
        try:
            info=extraer_info(cursor_server,tabla,"sqlserver")
        except Exception as e:
            print(f"Migration error in extraction of rows, {str(e)}")
        #SAQUE COLUMNAS NOMBRES DE SQLSERVER
        try:
            columnas=extraer_columnas(cursor_server,tabla,"sqlserver")
            columnas.append("fecha_modificacion")
        except Exception as e:
            print(f"Column names extraction error, {str(e)}")
        #EXTRAER TIPO DE DATO CON COLUMNAS JUNTA
        try:
            tipo_datos=extraer_tipo_datos(cursor_server,tabla,"sqlserver")
        except Exception as e:
            print(f"Error in extraction of data types, {str(e)}")
        # Crear la tabla en MySQL si no existe
        try:
            insertar_tabla(mycursor,tabla,tipo_datos)
        except Exception as e:
            print(f"Create table error, {str(e)}")
        # Insertar los datos en MySQL
        try:
            insertar_info(mycursor,tabla,columnas,info)
        except Exception as e:
            print(f"Error in the process of inserting information to mysql, {str(e)}")

        conexion_db.mydb.commit()
except Exception as e:
    print(f"Migration Error, {str(e)}")
#Ejecutando pruebas
try:
    pruebas=Pruebas(mycursor,cursor_server)
    pruebas.ejecutar_pruebas()

except Exception as e:
    print(f"Pruebas Error, {str(e)}")

finally:
    #Cerrando conexiones
    try:
        conexion_db.cerrar_conexiones()
    except Exception as e:
        print("Error in closing conexions in migration document")