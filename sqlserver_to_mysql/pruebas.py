import mysql.connector
import pyodbc
from dataclasses import dataclass
from extraccion_datos import obtener_tablas,extraer_columnas,extraer_numero_registros,extraer_info

@dataclass
class Pruebas:
    mycursor:any
    cursor_server:any
    #TRANSFORMA UNA LISTA DE TUPLAS A UNA LISTA DE STRING PARA LA COMPARACION DEL ASSERT
    def lista_tuplas_a_string(self,info):
        try:
            informacion = []
            for fila in info:
                informacion.append(str(fila))
            return informacion
        except Exception as e:
            print(f"Error in document Pruebas, with the lista_tuplas_a_string,{str(e)}")
            return 
    #COMPRUEBA QUE LA CANTIDAD DE LINEAS EN SQLSERVER SEA LA MISMA QUE EN MYSQL
    def comprobar_registros(self, tabla):
        try:
            registros_mysql = extraer_numero_registros(self.mycursor,tabla)
            registros_sqlserver = extraer_numero_registros(self.cursor_server,tabla)
            assert registros_mysql == registros_sqlserver, f"Error en la tabla {tabla} en cantidad de registros"
            
        except Exception as e:
            print(f"Pruebas error in comprobar_registros, {str(e)}")
            return
    #COMPRUEBA QUE LA INFORMACION DE UNA TABLA SEA IGUAL ENTRE SQLSERVER Y MYSQL
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
            return 
    def comprobar_querys(self,query):
        try:
            self.mycursor.execute(query)
            resultado1=self.mycursor.fetchall()
            query1_resultado1=self.lista_tuplas_a_string(resultado1)

            self.cursor_server.execute(query)
            resultado2=self.cursor_server.fetchall()
            query1_resultado2=self.lista_tuplas_a_string(resultado2)

            assert sorted(query1_resultado1)==sorted(query1_resultado2), "Error en el caso de prueba 1"
        except Exception as e:
            print(f"Error in comprobar_query, {str(e)}")
    def casos_prueba(self):
        try:
            #LIBRO PRESTADO POR CADA USUARIO
            query1=""" 
            SELECT u.usuario_id, u.nombre, COUNT(dp.libro_id) AS total_libros_prestados
            FROM usuario u
            JOIN prestamo p ON u.usuario_id = p.usuario_id
            JOIN detalle_prestamo dp ON p.prestamo_id = dp.prestamo_id
            GROUP BY u.usuario_id, u.nombre
            ORDER BY total_libros_prestados DESC;
            """
            self.comprobar_querys(query1)
            #Prestamos realizados por biblitecarios
            query2="""
            SELECT b.bibliotecario_id, b.nombre, COUNT(p.prestamo_id) AS total_prestamos
            FROM bibliotecario b
            JOIN prestamo p ON b.bibliotecario_id = p.bibliotecario_id
            GROUP BY b.bibliotecario_id, b.nombre
            ORDER BY total_prestamos DESC;
            """
            self.comprobar_querys(query2)
            #LIBRO POR CATEGORIA Y AUTOR
            query3="""
            SELECT c.nombre_categoria AS categoria, a.nombre AS autor, COUNT(l.libro_id) AS total_libros
            FROM categoria c
            JOIN libro l ON c.categoria_id = l.categoria_id
            JOIN libro_autor la ON l.libro_id = la.libro_id
            JOIN autor a ON la.autor_id = a.autor_id
            GROUP BY c.nombre_categoria, a.nombre
            ORDER BY total_libros DESC;
            """
            self.comprobar_querys(query3)
        except Exception as e:
            print(f"Error in casos_prueba, {str(e)}")

    #EJECUTA TODAS LAS PRUEBAS, COMPROBANDO CADA TABLA
    def ejecutar_pruebas(self):
        try:
            tablas_mysql = obtener_tablas(self.mycursor,"mysql")
            tablas_sqlserver = obtener_tablas(self.cursor_server,"sqlserver")
            if sorted(tablas_mysql)==sorted(tablas_sqlserver):
                for tabla in tablas_mysql:
                    self.comprobar_registros(tabla)
                    self.comprobar_contenido(tabla)
                    print(f"Tabla {tabla} realizado")
                self.casos_prueba()
                print("Casos de Prueba realizados")
            else:
                print("Number of tables test error")
        except Exception as e:
            print(f"Pruebas error in ejecutar_pruebas, {str(e)}")
            return

