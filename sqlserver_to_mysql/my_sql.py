import mysql.connector

conn_mysql = mysql.connector.connect(
    host="final",  # O el nombre de tu servidor MySQL
    user="root",  # O el nombre de usuario de MySQL
)

# Crear un cursor para ejecutar los comandos SQL
cursor_mysql = conn_mysql.cursor()

# Crear la base de datos (asegúrate de que el nombre de la base de datos no exista ya)
nombre_base_de_datos = "BibliotecaUniversitariaMySql"
cursor_mysql.execute(f"DROP DATABASE IF EXISTS {nombre_base_de_datos}")
cursor_mysql.execute(f"CREATE DATABASE {nombre_base_de_datos}")

# Confirmar los cambios
conn_mysql.commit()

print(f"Base de datos {nombre_base_de_datos} creada exitosamente.")

cursor_mysql.close()
conn_mysql.close()
