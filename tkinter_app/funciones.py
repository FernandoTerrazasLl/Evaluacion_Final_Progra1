from tkinter import messagebox
from datetime import datetime

# Visualizar Datos
def fetch_data(db_connection, tree, table_name):
    conn=db_connection.mydb
    if not conn:
        return
    cursor=conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows=cursor.fetchall()
        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo recuperar datos de {table_name}: {e}")
    finally:
        pass

# Añadir datos
def add_data(db_connection, tree, table_name, columns, values):
    conn=db_connection.mydb
    if not conn:
        return
    
    # Validación para la tabla Prestamo
    if table_name=="prestamo":
        try:
            fecha_prestamo_index=columns.index("fecha_prestamo")
            fecha_devolucion_index=columns.index("fecha_devolucion")
            fecha_limite_devolucion_index=columns.index("fecha_limite_devolucion")

            fecha_prestamo=datetime.strptime(values[fecha_prestamo_index], "%Y-%m-%d")
            fecha_devolucion=datetime.strptime(values[fecha_devolucion_index], "%Y-%m-%d")
            fecha_limite_devolucion=datetime.strptime(values[fecha_limite_devolucion_index], "%Y-%m-%d")

            if fecha_prestamo>fecha_devolucion:
                messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha de devolución.")
                return
            if fecha_prestamo>fecha_limite_devolucion:
                messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha límite de devolución.")
                return
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use AAAA-MM-DD.")
            return
    
    values=[value if value.strip() else None for value in values]
    cursor=conn.cursor()
    try:
        # Verificar si la tabla tiene columna fecha_modificacion
        cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE 'fecha_modificacion'")
        fecha_mod_exists=cursor.fetchone() is not None

        if fecha_mod_exists:
            # Agregar fecha_modificacion automáticamente
            columns.append('fecha_modificacion')
            values.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        placeholders=", ".join(["%s"] * len(values))
        query=f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Éxito", f"Registro agregado a {table_name}.")
        fetch_data(db_connection, tree, table_name)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el registro a {table_name}: {e}")
    finally:
        pass

# Eliminar datos
def delete_data(db_connection, tree, table_name, id_column):
    selected_item=tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Selecciona un registro para eliminar.")
        return
    # Mensaje de Confirmación eliminar registro
    confirm=messagebox.askquestion("Confirmación", "¿Estás seguro que deseas eliminar el registro?", icon='warning')
    if confirm != 'yes':
        return
    conn=db_connection.mydb
    if not conn:
        return
    cursor=conn.cursor()
    try:
        record_id=tree.item(selected_item)["values"][0]
        query=f"DELETE FROM {table_name} WHERE {id_column} = %s"
        cursor.execute(query, (record_id,))
        conn.commit()
        messagebox.showinfo("Éxito", f"Registro eliminado de {table_name}.")
        fetch_data(db_connection, tree, table_name)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el registro de {table_name}: {e}")
    finally:
        pass

# Modificar datos
def update_data(db_connection, tree, table_name, columns, values, record_id):
    conn=db_connection.mydb
    if not conn:
        return
    
    # Validación para la tabla Prestamo
    if table_name=="prestamo":
        try:
            fecha_prestamo_index=columns.index("fecha_prestamo")
            fecha_devolucion_index=columns.index("fecha_devolucion")
            fecha_limite_devolucion_index=columns.index("fecha_limite_devolucion")

            fecha_prestamo=datetime.strptime(values[fecha_prestamo_index], "%Y-%m-%d")
            fecha_devolucion=datetime.strptime(values[fecha_devolucion_index], "%Y-%m-%d")
            fecha_limite_devolucion=datetime.strptime(values[fecha_limite_devolucion_index], "%Y-%m-%d")

            if fecha_prestamo>fecha_devolucion:
                messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha de devolución.")
                return
            if fecha_prestamo>fecha_limite_devolucion:
                messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha límite de devolución.")
                return
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use AAAA-MM-DD.")
            return
    
    processed_values=[None if value.strip()=="" else value for value in values]
    cursor=conn.cursor()
    try:
        # Ver si la tabla tiene columna fecha_modificacion
        cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE 'fecha_modificacion'")
        fecha_mod_exists=cursor.fetchone() is not None

        if fecha_mod_exists:
            # Agregar fecha_modificacion automáticamente
            columns.append('fecha_modificacion')
            values.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        set_clause=", ".join([f"{col} = %s" for col in columns])
        query=f"UPDATE {table_name} SET {set_clause} WHERE {columns[0]} = %s"
        cursor.execute(query, processed_values + [record_id])
        conn.commit()
        messagebox.showinfo("Éxito", f"Registro actualizado en {table_name}.")
        fetch_data(db_connection, tree, table_name)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el registro de {table_name}: {e}")
    finally:
        pass