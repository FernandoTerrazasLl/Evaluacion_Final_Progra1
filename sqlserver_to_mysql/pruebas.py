import mysql.connector
import pyodbc
from dataclasses import dataclass

@dataclass
class Pruebas:
    mycursor:any
    cursor_server:any
    
    def obtener_tablas(self, cursor):
        tablas = []

        if cursor == self.mycursor:
            cursor.execute("SHOW TABLES;")
        else:
            cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' and TABLE_NAME !='sysdiagrams';")
        
        resultados = cursor.fetchall()
        for tabla in resultados:
            tablas.append(tabla[0])

        return tablas

    def extraer_numero_regitros(self,cursor,registros):
        cursor.execute(f"SELECT COUNT(*) FROM {registros};")
        return cursor.fetchone()[0]

    def comprobar_registros(self, registros):
        registros_mysql = self.extraer_numero_regitros(self.mycursor,registros)
        registros_sqlserver = self.extraer_numero_regitros(self.cursor_server,registros)

        assert registros_mysql == registros_sqlserver, f"Error en la tabla {registros} en cantidad de registros"

    def extraer_info(self,cursor,tabla):
        cursor.execute(f"SELECT * FROM {tabla};")
        tablas= cursor.fetchall()
        #ERROR AL COMPARAR CON ASSERT POR EL TIPO DE DATO, ENTONCES PARA COMPARAR LO VOLVEMOS STRING
        tabla_para_comparacion=[]
        for valor in tablas:
            tabla_para_comparacion.append(str(valor))
        return tuple(tabla_para_comparacion)
            

    def comprobar_contenido(self, tabla):
        # Extraer la información de ambas bases de datos
        info_mysql = self.extraer_info(self.mycursor, tabla)
        info_sqlserver = self.extraer_info(self.cursor_server, tabla)

        assert sorted(info_mysql) == sorted(info_sqlserver), f"Diferencia de contenido en tabla {tabla}"

    def ejecutar_pruebas(self):
        tablas_mysql = self.obtener_tablas(self.mycursor)
        tablas_sqlserver = self.obtener_tablas(self.cursor_server)

        if sorted(tablas_mysql)==sorted(tablas_sqlserver):
            for tabla in tablas_mysql:
                self.comprobar_registros(tabla)  
                self.comprobar_contenido(tabla)  
                print(f"Tabla '{tabla}' correcta")
        else:
            print("Number of tables test error")

