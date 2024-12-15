#AGREGAR COLUMNA EXTRA EN LA INTERFAZ FUSIONANDO LOS NOMBRES Y APELLIDO DE LOS BIBLITOCARIOS PERO CON PARENTESIS ENTRE LAS LETRAS APLICANDO RECURSIVIDAD
def recursividad(cursor,iterador,solucion):
    if iterador>4:
        return solucion

    cursor.execute(f"SELECT top {iterador} NOMBRE, APELLIDO FROM bibliotecario")
    solucion=cursor.fetchall()
    iterador +=1
    return recursividad(cursor,iterador,solucion)

def defensa(cursor):
    resolucion=recursividad(cursor,1,[])
    nombre_completo=[]
    for nombre_apellido in resolucion:
        nombre=nombre_apellido[0]
        apellido=nombre_apellido[1]
        nombre_completo.append(nombre+apellido)
        #LISTA DE LOS NOMBRES COMPLETOS HASTA AQUI CORRECTO
        #['Juan Pérez', 'María González', 'Carlos Ramírez', 'Ana López']

    solucion=[]
    for parentesis in nombre_completo:
        #Juan Perez
        longitud=len(parentesis)/2
        i=0
        persona=""
        for modificacion in parentesis:
            #J
            if modificacion !="'":
                if i<=longitud:
                    persona +=f"({modificacion}"
                else:
                    persona +=f"){modificacion}"
                i +=1
        persona +=")"
        solucion.append(persona)
    return solucion

def add_registro_defensa(db_connection, table_name="bibliotecario"):
    conn = db_connection.mydb
    server=db_connection.serverdb

    cursor = conn.cursor()
    server_cursor = server.cursor()
    #RESULTADO DE PARENTESIS A INSERTAR
    nombres = defensa(server_cursor)

    try:
        cursor.execute(f"ALTER TABLE {table_name} ADD defensa VARCHAR(255)")

        cursor.execute(f"SELECT {table_name}_id FROM {table_name}")
        rows = cursor.fetchall()

        for i, row in enumerate(rows):
            record_id = row[0]
            cursor.execute(f"UPDATE {table_name} SET defensa = %s WHERE {table_name}_id = %s", (nombres[i], record_id))
        conn.commit()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        server_cursor.close()