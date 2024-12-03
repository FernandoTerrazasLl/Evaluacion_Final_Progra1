from my_sql import *
from sql_server import *
#NOMBRE TABLAS
cursor_server.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' and TABLE_NAME !='sysdiagrams';")
tablas_nombres=cursor_server.fetchall()

#FILAS INFO DE LA TABLA
for tabla in tablas_nombres:
    tabla_nombre=tabla[0]
    cursor_server.execute(f"SELECT * FROM {tabla_nombre};")
    info=cursor_server.fetchall()
    
    #SAQUE COLUMNAS NOMBRES
    columnas = []  
    for columna in cursor_server.description:
        columnas.append(columna[0]) 
    

    tipo_datos=[]
    for columna in cursor_server.description:
        if int == (columna[1]):
            tipo_datos.append(f"{columna[0]} INT")
        elif str == (columna[1]):
            tipo_datos.append(f"{columna[0]} VARCHAR(255)")
        else:
            tipo_datos.append(f"{columna[0]} DATETIME")
    # Crear la tabla en MySQL si no existe
    mycursor.execute(f"CREATE TABLE IF NOT EXISTS {tabla_nombre} ({', '.join(tipo_datos)});")
    # Insertar los datos en MySQL
    for row in info:
        print(row)
        insert_query = f"INSERT INTO {tabla_nombre} ({', '.join(columnas)}) VALUES {row};"
        mysql_cursor.execute(insert_query)

    mysql_conn.commit()
    print(f"Tabla {tabla_nombre} migrada con éxito.")



