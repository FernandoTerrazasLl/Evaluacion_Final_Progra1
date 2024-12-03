from my_sql import *
from sql_server import *
#NOMBRE TABLAS
try:
    cursor_server.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' and TABLE_NAME !='sysdiagrams';")
    tablas_nombres=cursor_server.fetchall()
except:
    print("Not able to find table names")

#FILAS INFO DE LA TABLA
try:
    for tabla in tablas_nombres:
        try:
            tabla_nombre=tabla[0]
            cursor_server.execute(f"SELECT * FROM {tabla_nombre};")
            info=cursor_server.fetchall()
        except:
            print("Table name not found")
        
        try:
            #SAQUE COLUMNAS NOMBRES
            columnas = []  
            for columna in cursor_server.description:
                columnas.append(columna[0]) 
        except:
            print("Column names extraction error")
        
        try:
            tipo_datos=[]
            i=1
            for columna in cursor_server.description:
                if int == (columna[1]):
                    tipo ="INT"
                elif str == (columna[1]):
                    tipo="VARCHAR(255)"
                else:
                    tipo="DATETIME"
                
                if i==1:
                    tipo +=" PRIMARY KEY"
                
                tipo_datos.append(f"{columna[0]} {tipo}")
                i +=1
        except:
            print("Data type error")

        # Crear la tabla en MySQL si no existe
        try:
            mycursor.execute(f"CREATE TABLE IF NOT EXISTS {tabla_nombre} ({', '.join(tipo_datos)});")
        except:
            print("Create table error")
        # Insertar los datos en MySQL
        try:
            for row in info:
                placeholders = ", ".join(["%s"] * len(row))
                insert_query = f"INSERT INTO {tabla_nombre} ({', '.join(columnas)}) VALUES ({placeholders})"
                mycursor.execute(insert_query, tuple(row))  #
        except:
            print("Insert info error")

        mydb.commit()
except:
    print("Migration Error")


#PRUEBA PARA JOINS: SELECT p.estado,p.fecha_prestamo FROM Bibliotecario b inner JOIN Prestamo p ON b.bibliotecario_id = p.bibliotecario_id
mycursor.execute("Select * from autor")
rows=mycursor.fetchall()
print(rows)






