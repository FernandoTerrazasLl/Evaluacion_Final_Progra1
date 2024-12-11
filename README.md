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
PARA EL ARCHIVO CONEXION:
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
## Características Principales

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
- Comparación de contenido de registros y conteo de filas.
- Uso de `assert` para asegurar consistencia de datos.

## Casos de Uso

###

## VIDEO EXPLICATIVO PARA USO DE LA INTERFAZ

## Autores
- Fernando Terrazas
- Ariany Lopez

