# Proyecto: Modernización del Sistema de Gestión de Datos

## **Definición del Problema**

La empresa enfrenta un problema crítico de gestión de datos debido a un sistema heredado basado en tecnología obsoleta. Este sistema es lento, propenso a inconsistencias y carece de escalabilidad. La tarea consiste en diseñar e implementar un nuevo sistema utilizando bases de datos relacionales y una aplicación Python moderna que garantice eficiencia, confiabilidad y facilidad de uso.

## **Objetivos del Proyecto**

1. Migrar datos de un sistema obsoleto (SQLSERVER) a una nueva base de datos (MYSQL).
2. Diseñar una aplicación en Python para gestionar los datos con:
   - Procedimientos almacenados.
   - Integridad de la información.
   - Conexión eficiente y segura con las bases de datos.
3. Implementar una interfaz de usuario con Python y Tkinter para facilitar la administración de los datos migrados.

## DIAGRAMA ENTIDAD-RELACION
El diagrama entidad-relacion usado para la base de datos antigua (SQLSERVER) es:

![Diagrama Entidad-Relacion FINAL (1)](https://github.com/user-attachments/assets/5312bb24-af3b-403b-b1d7-c363bb45953e)
# Migracion de Base de Datos

## DIAGRAMA DE CLASES
Diagramas de clases usados durante la migracion de datos:

![Diagrama_clases_migracion drawio](https://github.com/user-attachments/assets/55d244fc-ec5a-4229-ad28-70507201668c)
## PSEUDOCODIGO
Para el archivo conexion:
```
CLASE Conexiones:
    ATRIBUTOS:
        mydb = NULO
        serverdb = NULO

    MÉTODO crear_base_datos():
        TRATAR:
            SI mydb está conectado:
                Crear un cursor (mycursor)
                Ejecutar las siguientes sentencias SQL:
                    1. Eliminar la base de datos "BibliotecaUniversidad" si existe
                    2. Crear la base de datos "BibliotecaUniversidad" si no existe
                    3. Usar la base de datos "BibliotecaUniversidad"
                Cerrar el cursor
        GESTIONAR ERROR:
            Mostrar "Error en la creación de la base de datos"

    MÉTODO conectar_mysql():
        TRATAR:
            Conectar a MySQL usando:
                - host = "localhost"
                - user = "root"
                - port = "3306"
                - password = "#CONTRASEÑA"
                - auth_plugin = "mysql_native_password"
            GUARDAR la conexión en mydb
            LLAMAR a crear_base_datos()
        GESTIONAR ERROR:
            Mostrar "Error al conectar con MySQL"

    MÉTODO conectar_sqlserver():
        Configurar los parámetros de conexión para SQL Server:
            - server = "#EDITAR"
            - database = "BibliotecaUniversitaria"
            - username = "#EDITAR"
        TRATAR:
            Conectar a SQL Server usando los parámetros
            GUARDAR la conexión en serverdb
        GESTIONAR ERROR:
            Mostrar "Error al conectar con SQL Server"

    MÉTODO cerrar_conexiones():
        TRATAR:
            SI mydb está conectado:
                Cerrar la conexión a MySQL
        GESTIONAR ERROR:
            Mostrar "Error al cerrar la conexión con MySQL"

        TRATAR:
            SI serverdb está conectado:
                Cerrar la conexión a SQL Server
        GESTIONAR ERROR:
            Mostrar "Error al cerrar la conexión con SQL Server"
```
Para el archivo extraccion_datos:
```
INICIAR función obtener_tablas(cursor, base_datos)
    INICIALIZAR lista vacía tablas
    INTENTAR
        SI base_datos ES "mysql"
            EJECUTAR consulta: "SHOW TABLES;"
        SINO
            EJECUTAR consulta: 
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME != 'sysdiagrams';"
        OBTENER resultados de cursor.fetchall()
        PARA cada tabla EN resultados
            AGREGAR tabla[0] A tablas
        IMPRIMIR tablas
        RETORNAR tablas
    Excepción error
        IMPRIMIR "pruebas error in obtener_tablas" y mensaje de error
FINALIZAR función

INICIAR función extraer_numero_registros(cursor, tabla)
    INTENTAR
        EJECUTAR consulta: "SELECT COUNT(*) FROM {tabla};"
        OBTENER numero_registros de cursor.fetchone()[0]
        RETORNAR numero_registros
    Excepción error
        IMPRIMIR "Pruebas error in extraer_numero_registros" y mensaje de error
FINALIZAR función

INICIAR función extraer_columnas(cursor, tabla, base_datos)
    INTENTAR
        SI base_datos ES "mysql"
            EJECUTAR consulta: "SELECT * FROM {tabla} LIMIT 1;"
        SINO
            EJECUTAR consulta: "SELECT TOP 1 * FROM {tabla};"
        INICIALIZAR lista vacía columnas
        PARA cada columna EN cursor.description
            AGREGAR columna[0] A columnas
        LLAMAR cursor.fetchall() PARA consumir resultados
        RETORNAR columnas
    Excepción error
        IMPRIMIR "Error in extraction of columns"
FINALIZAR función

INICIAR función extraer_info(cursor, tabla, base_datos)
    INTENTAR
        OBTENER columnas llamando extraer_columnas(cursor, tabla, base_datos)
        SI "fecha_modificacion" ESTÁ EN columnas
            REMOVER "fecha_modificacion" DE columnas
        UNIR columnas en una cadena separada por comas (columnas_query)
        EJECUTAR consulta: "SELECT {columnas_query} FROM {tabla};"
        OBTENER info de cursor.fetchall()
        RETORNAR info
    Excepción error
        IMPRIMIR "Pruebas error in extraer_info" y mensaje de error
FINALIZAR función

INICIAR función extraer_tipo_datos(cursor, tabla, base_datos)
    INTENTAR
        OBTENER columnas llamando extraer_columnas(cursor, tabla, base_datos)
        AGREGAR "fecha_modificacion" A columnas
        INICIALIZAR lista vacía tipo_datos y contador i=1
        PARA cada columna EN cursor.description
            SI columna[1] ES int
                tipo = "INT"
            SI columna[1] ES str
                tipo = "VARCHAR(255)"
            EN OTRO CASO
                tipo = "DATE"
            SI i ES 1
                CONCATENAR " AUTO_INCREMENT PRIMARY KEY" a tipo
            AGREGAR "{columna[0]} {tipo}" A tipo_datos
            INCREMENTAR i EN 1
        AGREGAR "fecha_modificacion DATE" A tipo_datos
        RETORNAR tipo_datos
    Excepción error
        IMPRIMIR "Data type error" y mensaje de error
FINALIZAR función
```
Para el archivo insertar_datos:
```
Función insertar_tabla(cursor, tabla, tipo_datos):
    Intentar:
        Ejecutar una sentencia SQL para crear una tabla en la base de datos:
            - Nombre de la tabla: `tabla`
            - Tipos de datos de las columnas: `tipo_datos`
            - Si la tabla ya existe, no se realiza ninguna acción (CREATE TABLE IF NOT EXISTS)
    Excepción:
        Si ocurre un error:
            Imprimir un mensaje de error que incluya detalles sobre el error

Función insertar_info(cursor, tabla, columnas, info):
    Intentar:
        Para cada fila en la lista `info`:
            - Preparar una cadena de texto con placeholders (marcadores de posición) para los valores
            - Construir una consulta SQL para insertar los datos en la tabla `tabla`
            - Ejecutar la consulta de inserción usando los datos de la fila
    Excepción:
        Si ocurre un error:
            Imprimir un mensaje de error que incluya detalles sobre el error
```
Para el archivo pruebas:
```
Clase Pruebas:
    Atributos:
        mycursor: cursor para la base de datos MySQL
        cursor_server: cursor para el servidor de SQL Server

    Método lista_tuplas_a_string(info):
        Intentar:
            Crear una lista vacía llamada `informacion`
            Para cada fila en `info`:
                Convertir la fila a cadena y agregarla a la lista `informacion`
            Retornar la lista `informacion`
        Excepción:
            Si ocurre un error:
                Imprimir el error con el mensaje "Error in document Pruebas, with the lista_tuplas_a_string"

    Método comprobar_registros(tabla):
        Intentar:
            Obtener el número de registros de la tabla en MySQL usando `extraer_numero_registros`
            Obtener el número de registros de la tabla en SQL Server usando `extraer_numero_registros`
            Comprobar si el número de registros en ambas bases de datos es el mismo
            Si no son iguales, lanzar un error con el mensaje correspondiente
        Excepción:
            Si ocurre un error:
                Imprimir el error con el mensaje "Pruebas error in comprobar_registros"

    Método comprobar_contenido(tabla):
        Intentar:
            Extraer la información de la tabla de MySQL usando `extraer_info`
            Convertir la información extraída de MySQL a una lista de cadenas usando `lista_tuplas_a_string`
            Extraer la información de la tabla de SQL Server usando `extraer_info`
            Convertir la información extraída de SQL Server a una lista de cadenas usando `lista_tuplas_a_string`
            Comparar las listas ordenadas de MySQL y SQL Server
            Si son diferentes, lanzar un error con el mensaje correspondiente
        Excepción:
            Si ocurre un error:
                Imprimir el error con el mensaje "Pruebas error in comprobar_contenido"

    Método ejecutar_pruebas():
        Intentar:
            Obtener la lista de tablas de MySQL usando `obtener_tablas`
            Obtener la lista de tablas de SQL Server usando `obtener_tablas`
            Comparar las listas de tablas de ambas bases de datos
            Si las listas son iguales, para cada tabla:
                Ejecutar las pruebas de registros con `comprobar_registros`
                Ejecutar las pruebas de contenido con `comprobar_contenido`
                Imprimir un mensaje que indique que la tabla es correcta
            Si las listas no son iguales, imprimir un mensaje de error en la comparación de tablas
        Excepción:
            Si ocurre un error:
                Imprimir el error con el mensaje "Pruebas error in ejecutar_pruebas"
```
Para el archivo migration_main:
```
# Estableciendo las conexiones a las bases de datos
LLAMANDO A conectar_mysql
LLAMANDO A conectar_sqlserver

# Creando los cursores para las consultas
LLAMANDO A mydb.cursor
LLAMANDO A serverdb.cursor

# Obtener los nombres de las tablas en SQL Server
LLAMANDO A obtener_tablas

Para cada tabla en las tablas obtenidas:
    Intentar:
        # Extraer la información de la tabla de SQL Server
        LLAMANDO A extraer_info
    Excepción:
        Si ocurre un error:
            Imprimir el error de extracción de filas

    Intentar:
        # Extraer los nombres de las columnas de la tabla en SQL Server
        LLAMANDO A extraer_columnas
        LLAMANDO A append "fecha_modificacion" a columnas
    Excepción:
        Si ocurre un error:
            Imprimir el error de extracción de columnas

    Intentar:
        # Extraer los tipos de datos de las columnas en SQL Server
        LLAMANDO A extraer_tipo_datos
    Excepción:
        Si ocurre un error:
            Imprimir el error de extracción de tipos de datos

    Intentar:
        # Crear la tabla en MySQL si no existe
        LLAMANDO A insertar_tabla
    Excepción:
        Si ocurre un error:
            Imprimir el error de creación de la tabla

    Intentar:
        # Insertar los datos en MySQL
        LLAMANDO A insertar_info
    Excepción:
        Si ocurre un error:
            Imprimir el error de inserción de datos

    LLAMANDO A commit

Excepción:
    Si ocurre un error en el proceso de migración:
        Imprimir el error general de migración

# Ejecutar las pruebas de migración
Intentar:
    LLAMANDO A Pruebas
    LLAMANDO A ejecutar_pruebas
Excepción:
    Si ocurre un error en las pruebas:
        Imprimir el error de pruebas

# Cerrar las conexiones
Finalmente:
    Intentar:
        LLAMANDO A cerrar_conexiones
    Excepción:
        Si ocurre un error al cerrar las conexiones:
            Imprimir el error al cerrar las conexiones
```
# Interfaz

## DIAGRAMA DE CLASES

## PSEUDOCODIGO

### Aplicación GUI con Tkinter

- Visualización de registros.
- Inserción, modificación y eliminación de datos.
- Validación de entradas del usuario.
- Manejo seguro de conexiones a bases de datos.

### Pruebas

- Verificación de integridad de datos entre tablas de SQLSERVER y MYSQL.
- Comparación de contenido de registros y conteo de filas totales.
- Uso de `assert` para asegurar consistencia de datos.

## Casos de Uso

###

## VIDEO EXPLICATIVO PARA USO DE LA INTERFAZ

## Autores
- Fernando Terrazas
- Ariany Lopez

