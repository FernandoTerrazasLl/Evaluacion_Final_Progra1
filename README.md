# Proyecto: Modernización del Sistema de Gestión de Datos

## **Definición del Problema**

La empresa enfrenta un problema crítico de gestión de datos debido a un sistema heredado basado en tecnología obsoleta. Este sistema es lento, propenso a inconsistencias y carece de escalabilidad. La tarea consiste en diseñar e implementar un nuevo sistema utilizando bases de datos relacionales y una aplicación Python moderna que garantice eficiencia, confiabilidad y facilidad de uso.

## **Objetivos del Proyecto**

1. Migrar datos de un sistema obsoleto (SQLSERVER) a una nueva base de datos (MYSQL).
2. Diseñar una aplicación en Python para gestionar los datos
3. Implementar una interfaz de usuario con Python y Tkinter para facilitar la administración de los datos migrados.

## DIAGRAMA ENTIDAD-RELACION
El diagrama entidad-relacion usado para la base de datos antigua (SQLSERVER) es:

![Diagrama Entidad-Relacion FINAL (1)](https://github.com/user-attachments/assets/5312bb24-af3b-403b-b1d7-c363bb45953e)

La base de datos nueva tendra la misma estructura, solamente se le adiccioanra un atributo extra a cada tabla respecto a la fecha de modificacion mas reciente de dichos registros.
# Migracion de Base de Datos

## Requisitos para la Migración

1. **Script para la Migración:**
   - Utilizar Python y bibliotecas compatibles para la conexión con bases de datos.
   - Crear un script que migre los datos de una base de datos en SQLSERVER a un nuevo manejador, como MYSQL.
   - Modificar el esquema original si es necesario mediante sentencias SQL.

2. **Criterios de Finalización:**
   - Todas las tablas deben aparecer en el nuevo manejador de base de datos tras ejecutar el script.
   - Todas las relaciones entre registros deben mantenerse intactas.
   - El script debe emplear `dataclass` para la definición de estructuras de datos.
   - La ejecución repetida del script no debe generar registros duplicados en la base de datos de destino.
   - El código debe incluir manejo de errores para operaciones de lectura y escritura.
   - conexiones solo una vez al inicio del programa.
   - Manejarse con bloques `try`, `except`, y `finally` para asegurar su cierre adecuado.

## Requisitos de las Pruebas
   - Asegurarse de que el código de migración de datos funcione correctamente entre SQLSERVER y MYSQL.
   - Comparar el número de registros en cada tabla de SQLSERVER y MYSQL para garantizar que coincidan.
   - Comprobar que los valores de los campos en cada registro sean iguales en ambas bases de datos.
   - Escribir pruebas que validen el contenido y la estructura de las tablas migradas.
   - Usar `assert` para comparar los datos esperados con los datos reales.
   - Diseñar casos de prueba para garantizar que las relaciones entre los registros también se mantengan.

## DIAGRAMA DE CLASES
Diagramas de clases usados durante la migracion de datos:

![Diagrama_clases_migracion drawio (2)](https://github.com/user-attachments/assets/b33aa3b9-15ca-4533-a0e4-65a03679c1bc)
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
Para el archivo main.py:
```
INICIO
    DEFINIR conexion_db COMO Instancia de Conexiones

    # Conexión a la base de datos MySQL
    INTENTA
        conexion_db.conectar_mysql()
        SI conexion_db.mydb NO ESTÁ CONECTADA O conexion_db.mydb NO ES VÁLIDA
            LANZAR EXCEPCIÓN("Conexión a MySQL no establecida.")
    EXCEPTO Exception COMO e
        IMPRIMIR "Error al conectar a las bases de datos: " + e.mensaje
        SALIR(1)

    # Conexión a la base de datos SQL Server
    INTENTA
        conexion_db.conectar_sqlserver()
    EXCEPTO Exception COMO e
        IMPRIMIR "Error al conectar a las bases de datos: " + e.mensaje
        SALIR(1)

    # Creación de la base de datos y migración de datos
    INTENTA
        conexion_db.crear_base_datos()
        LLAMAR migration_main(conexion_db)
    EXCEPTO Exception COMO e
        IMPRIMIR "Error durante la creación de la base de datos o la migración: " + e.mensaje
        conexion_db.cerrar_conexiones()
        SALIR(1)

    # Iniciar la aplicación Tkinter
    INTENTA
        DEFINIR root COMO Tk()
        DEFINIR app COMO BibliotecaApp(root, conexion_db)
        LLAMAR root.mainloop()
    EXCEPTO Exception COMO e
        IMPRIMIR "Error al iniciar la aplicación Tkinter: " + e.mensaje
    FINALMENTE
        conexion_db.cerrar_conexiones()
FIN
```
Para el archivo funciones.py:
```
# Importar herramientas necesarias para mostrar mensajes y manejar fechas

FUNCION fetch_data(db_connection, table_name):
    conn = db_connection.mydb
    SI conn NO está disponible:
        TERMINAR
    cursor = conn.cursor()
    INTENTAR:
        # Ejecutar consulta para obtener todos los registros de la tabla
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # Mostrar los registros obtenidos
        IMPRIMIR "Datos obtenidos:"
        PARA CADA row EN rows:
            IMPRIMIR row
    EN CASO DE ERROR e:
        messagebox.showerror("Error", f"No se pudo recuperar datos de {table_name}: {e}")

FUNCION add_data(db_connection, table_name, columns, values):
    conn = db_connection.mydb
    SI conn NO está disponible:
        TERMINAR
    
    SI table_name ES "prestamo":
        INTENTAR:
            fecha_prestamo_index = columns.index("fecha_prestamo")
            fecha_devolucion_index = columns.index("fecha_devolucion")
            fecha_limite_devolucion_index = columns.index("fecha_limite_devolucion")

            fecha_prestamo = datetime.strptime(values[fecha_prestamo_index], "%Y-%m-%d")
            fecha_devolucion = datetime.strptime(values[fecha_devolucion_index], "%Y-%m-%d")
            fecha_limite_devolucion = datetime.strptime(values[fecha_limite_devolucion_index], "%Y-%m-%d")

            SI fecha_prestamo > fecha_devolucion:
                messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha de devolución.")
                TERMINAR
            SI fecha_prestamo > fecha_limite_devolucion:
                messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha límite de devolución.")
                TERMINAR
        EN CASO DE ERROR:
            messagebox.showerror("Error", "Formato de fecha inválido. Use AAAA-MM-DD.")
            TERMINAR
    
    values = [value SI value.strip() SINO None PARA value EN values]
    cursor = conn.cursor()
    INTENTAR:
        cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE 'fecha_modificacion'")
        fecha_mod_exists = cursor.fetchone() NO ES None

        SI fecha_mod_exists:
            columns.append('fecha_modificacion')
            values.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        placeholders = ", ".join(["%s"] * len(values))
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Éxito", f"Registro agregado a {table_name}.")
        fetch_data(db_connection, table_name)
    EN CASO DE ERROR e:
        messagebox.showerror("Error", f"No se pudo agregar el registro a {table_name}: {e}")

FUNCION delete_data(db_connection, table_name, id_column):
    selected_item = SELECCIONAR registro de la lista de datos
    SI selected_item ES None:
        messagebox.showerror("Error", "Selecciona un registro para eliminar.")
        TERMINAR

    confirm = messagebox.askquestion("Confirmación", "¿Estás seguro que deseas eliminar el registro?", icon='warning')
    SI confirm != 'yes':
        TERMINAR

    conn = db_connection.mydb
    SI conn NO está disponible:
        TERMINAR

    cursor = conn.cursor()
    INTENTAR:
        record_id = ID del registro seleccionado
        query = f"DELETE FROM {table_name} WHERE {id_column} = %s"
        cursor.execute(query, (record_id,))
        conn.commit()
        messagebox.showinfo("Éxito", f"Registro eliminado de {table_name}.")
        fetch_data(db_connection, table_name)
    EN CASO DE ERROR e:
        messagebox.showerror("Error", f"No se pudo eliminar el registro de {table_name}: {e}")

FUNCION update_data(db_connection, table_name, columns, values, record_id):
    conn = db_connection.mydb
    SI conn NO está disponible:
        TERMINAR

    INTENTAR:
        primary_key = f"{table_name}_id"

        SI table_name ES "prestamo":
            INTENTAR:
                FUNCION validar_fecha(col_name):
                    SI col_name EN columns:
                        fecha_str = values[columns.index(col_name)]
                        RETORNAR datetime.strptime(fecha_str, "%Y-%m-%d") SI fecha_str.strip() SINO None
                    RETORNAR None
                
                fecha_prestamo = validar_fecha("fecha_prestamo")
                fecha_devolucion = validar_fecha("fecha_devolucion")
                fecha_limite_devolucion = validar_fecha("fecha_limite_devolucion")

                SI fecha_prestamo Y fecha_devolucion Y fecha_prestamo > fecha_devolucion:
                    messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha de devolución.")
                    TERMINAR
                
                SI fecha_prestamo Y fecha_limite_devolucion Y fecha_prestamo > fecha_limite_devolucion:
                    messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha límite de devolución.")
                    TERMINAR

                SI "estado" EN columns Y values[columns.index("estado")] == "Devuelto":
                    SI NO fecha_devolucion:
                        messagebox.showerror("Error", "La fecha de devolución no puede estar vacía si el estado es 'Devuelto'.")
                        TERMINAR
            EN CASO DE ERROR e:
                messagebox.showerror("Error", f"Formato de fecha inválido. Use AAAA-MM-DD. Detalle: {e}")
                TERMINAR

        excluded_columns = [primary_key, 'fecha_modificacion']
        modifiable_columns = [col PARA col EN columns SI col NO EN excluded_columns]
        processed_values = [values[columns.index(col)] PARA col EN modifiable_columns]

        cursor = conn.cursor()
        cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE 'fecha_modificacion'")
        fecha_mod_exists = cursor.fetchone() NO ES None

        SI fecha_mod_exists:
            modifiable_columns.append('fecha_modificacion')
            processed_values.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        set_clause = ", ".join([f"{col} = %s" PARA col EN modifiable_columns])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {primary_key} = %s"
        cursor.execute(query, processed_values + [record_id])
        conn.commit()
        messagebox.showinfo("Éxito", f"Registro actualizado en {table_name}.")
        fetch_data(db_connection, table_name)
    EN CASO DE ERROR e:
        messagebox.showerror("Error", f"No se pudo actualizar el registro de {table_name}: {e}")
```
Para el archivo biblioteca_app.py:
```
CLASE BibliotecaApp:
    CONSTRUCTOR(root, db_connection):
        Establecer título de la ventana
        Establecer tamaño de la ventana
        Guardar conexión de base de datos
        Llamar a crear menú principal

    FUNCIÓN create_action_interface(self, action, table_name, columns, id_column):
        Limpiar widgets de la ventana
        Mostrar título de la acción
        Crear árbol (Treeview) con columnas
        Configurar encabezados y columnas del árbol
        Cargar datos de la tabla en el árbol
        
        SI acción es "eliminar":
            Crear botón de eliminar
        
        SI acción es "agregar" o "modificar":
            Crear formulario de entrada
        
        Crear botón de volver al menú anterior

    FUNCIÓN create_form(self, action, tree, table_name, columns, id_column):
        Crear marco para formulario
        Crear campos de entrada para cada columna
        
        SI acción es "agregar":
            Crear función para agregar datos
            Crear botón de agregar
        
        SI acción es "modificar":
            Crear función para cargar datos seleccionados
            Crear función para actualizar datos
            Añadir evento de selección
            Crear botón de modificar

    FUNCIÓN create_table_menu(self, action):
        Limpiar widgets de la ventana
        Definir diccionario de tablas con sus columnas
        
        Para cada tabla:
            Crear botón para seleccionar tabla
        
        Crear botón de volver al menú principal

    FUNCIÓN create_main_menu():
        Limpiar widgets de la ventana
        Mostrar título principal
        
        Para cada acción (visualizar, agregar, modificar, eliminar):
            Crear botón de acción que lleva al menú de tablas
```
### Casos de Uso del Proyecto
- Migracion entre Base de Datos efectiva incluyendo registros
- Visualización de registros.
- Inserción, modificación y eliminación de datos.
- Validación de entradas del usuario.
- Manejo seguro de conexiones a bases de datos.

### Pruebas

- Verificación de integridad de datos entre tablas de SQLSERVER y MYSQL.
- Comparación de contenido de registros y conteo de filas totales.
- Uso de `assert` para asegurar consistencia de datos.

## VIDEO EXPLICATIVO PARA USO DE LA INTERFAZ

## Autores
- Fernando Terrazas
- Ariany Lopez

