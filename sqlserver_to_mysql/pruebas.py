import mysql.connector
import pyodbc
from dataclasses import dataclass

@dataclass
class Pruebas:
    mycursor:any
    cursor_server:any
    
    def obtener_tablas(self, cursor):
        tablas = []
        try:
            if cursor == self.mycursor:
                cursor.execute("SHOW TABLES;")
            else:
                cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' and TABLE_NAME !='sysdiagrams';")
            
            resultados = cursor.fetchall()
            for tabla in resultados:
                tablas.append(tabla[0])
                
            return tablas
        except Exception as e:
            print(f"pruebas error in obtener_tablas, {str(e)}")

    def extraer_numero_registros(self,cursor,tabla):
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla};")
            numero_registros=cursor.fetchall()[0][0]
            print(numero_registros)

            if numero_registros is None:
                print("None")
            return numero_registros
            
        except Exception as e:
            print(f"Pruebas error in extraer_numero_registros, {str(e)}")

    def comprobar_registros(self, tabla):
        try:
            registros_mysql = self.extraer_numero_registros(self.mycursor,tabla)
            registros_sqlserver = self.extraer_numero_registros(self.cursor_server,tabla)
            assert registros_mysql == registros_sqlserver, f"Error en la tabla {tabla} en cantidad de registros"
        except Exception as e:
            print(f"Pruebas error in comprobar_registros, {str(e)}")

    def extraer_info(self,cursor,tabla):
        try:
            if cursor==self.mycursor:
                cursor.execute(f"SELECT * FROM {tabla} LIMIT 1;")#PARA TRAER SOLO LAS COLUMNAS
            else:
                cursor.execute(f"SELECT TOP 1 * FROM {tabla};")
            columnas = []
            for columna in cursor.description:
                columnas.append(columna[0])
                cursor.fetchall() #IMPORTANTE PARA LIMPIAR EL CURSOR (error memorable)

            if "fecha_modificacion" in columnas:
                columnas.remove("fecha_modificacion")

            columnas_query = ", ".join(columnas)
            if cursor==self.mycursor:
                cursor.execute(f"SELECT {columnas_query} FROM {tabla};")
            else:
                cursor.execute(f"SELECT {columnas_query} FROM [{tabla}];")
            info = cursor.fetchall()
            resultado = []

            for fila in info:
                resultado.append(str(fila))
            return tuple(resultado)
            
        except Exception as e:
            print(f"Pruebas error in extraer_info, {str(e)}")
            
    def comprobar_contenido(self, tabla):
        try:
            # Extraer la información de ambas bases de datos
            info_mysql = self.extraer_info(self.mycursor, tabla)
            info_sqlserver = self.extraer_info(self.cursor_server, tabla)

            assert sorted(info_mysql) == sorted(info_sqlserver), f"Diferencia de contenido en tabla {tabla}"
        except Exception as e:
            print(f"Pruebas error in comprobar_contenido, {str(e)}")

    def ejecutar_pruebas(self):
        try:
            tablas_mysql = self.obtener_tablas(self.mycursor)
            tablas_sqlserver = self.obtener_tablas(self.cursor_server)
            if sorted(tablas_mysql)==sorted(tablas_sqlserver):
                for tabla in tablas_mysql:
                    self.comprobar_registros(tabla)
                    self.comprobar_contenido(tabla)
                    print(f"Tabla '{tabla}' correcta")
            else:
                print("Number of tables test error")
        except Exception as e:
            print(f"Pruebas error in ejecutar_pruebas, {str(e)}")
