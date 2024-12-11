import mysql.connector
import pyodbc
from dataclasses import dataclass
from extraccion_datos import obtener_tablas,extraer_columnas,extraer_numero_registros,extraer_info

@dataclass
class Pruebas:
    mycursor:any
    cursor_server:any
    def lista_tuplas_a_string(self,info):
        try:
            informacion = []
            for fila in info:
                informacion.append(str(fila))
            return informacion
        except Exception as e:
            print(f"Error in document Pruebas, with the lista_tuplas_a_string,{str(e)}")

    def comprobar_registros(self, tabla):
        try:
            registros_mysql = extraer_numero_registros(self.mycursor,tabla)
            registros_sqlserver = extraer_numero_registros(self.cursor_server,tabla)
            assert registros_mysql == registros_sqlserver, f"Error en la tabla {tabla} en cantidad de registros"
            
        except Exception as e:
            print(f"Pruebas error in comprobar_registros, {str(e)}")

    def comprobar_contenido(self, tabla):
        try:
            # Extraer la información de ambas bases de datos
            info_mysql = extraer_info(self.mycursor, tabla,"mysql")
            info_mysql_transformada= self.lista_tuplas_a_string(info_mysql)
            info_sqlserver = extraer_info(self.cursor_server, tabla,"sqlserver")
            info_sqlserver_transformada= self.lista_tuplas_a_string(info_sqlserver)

            assert sorted(info_mysql_transformada) == sorted(info_sqlserver_transformada), f"Diferencia de contenido en tabla {tabla}"
        except Exception as e:
            print(f"Pruebas error in comprobar_contenido, {str(e)}")

    def ejecutar_pruebas(self):
        try:
            tablas_mysql = obtener_tablas(self.mycursor,"mysql")
            tablas_sqlserver = obtener_tablas(self.cursor_server,"sqlserver")
            if sorted(tablas_mysql)==sorted(tablas_sqlserver):
                for tabla in tablas_mysql:
                    self.comprobar_registros(tabla)
                    self.comprobar_contenido(tabla)
                    print(f"Tabla {tabla} correcta")
            else:
                print("Number of tables test error")
        except Exception as e:
            print(f"Pruebas error in ejecutar_pruebas, {str(e)}")
