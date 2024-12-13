from tkinter import messagebox
from datetime import datetime

# Visualizar Datos
def fetch_data(db_connection, tree, table_name):
    conn=db_connection.connect()
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
        conn.close()

# Añadir datos
def add_data(db_connection, tree, table_name, columns, values):
    conn=db_connection.connect()
    if not conn:
        return
    
    # Validación para la tabla Prestamo
    if table_name=="Prestamo":
        fecha_prestamo_index = columns.index("fecha_prestamo")
        fecha_devolucion_index = columns.index("fecha_devolucion")
        estado_index = columns.index("estado")
        
        fecha_prestamo=values[fecha_prestamo_index]
        fecha_devolucion = values[fecha_devolucion_index]
        estado = values[estado_index]
        
        # Si el estado es Activo, no debe haber fecha de devolución
        if estado=="Activo" and fecha_devolucion and fecha_devolucion.strip():
            messagebox.showerror("Error", "Un préstamo Activo no puede tener fecha de devolución.")
            return
        
        # Si hay fecha de devolución, validar que sea posterior a la fecha de préstamo
        if fecha_devolucion and fecha_devolucion.strip() and estado == "Devuelto":
            try:
                prestamo_date=datetime.strptime(fecha_prestamo, "%Y-%m-%d")
                devolucion_date=datetime.strptime(fecha_devolucion, "%Y-%m-%d")
                
                # Validar que la fecha de devolución sea posterior a la fecha de préstamo
                if devolucion_date<prestamo_date:
                    messagebox.showerror("Error", "La fecha de devolución debe ser posterior a la fecha de préstamo.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use AAAA-MM-DD")
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
        conn.close()

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
    conn=db_connection.connect()
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
        conn.close()

# Modificar datos
def update_data(db_connection, tree, table_name, columns, values, record_id):
    conn=db_connection.connect()
    if not conn:
        return
    
    # Validación para la tabla Prestamo
    if table_name=="Prestamo":
        fecha_prestamo_index=columns.index("fecha_prestamo")
        fecha_devolucion_index=columns.index("fecha_devolucion")
        estado_index=columns.index("estado")
        
        fecha_prestamo=values[fecha_prestamo_index]
        fecha_devolucion=values[fecha_devolucion_index]
        estado=values[estado_index]
        
        # Si el estado es Activo, no debe haber fecha de devolución
        if estado=="Activo" and fecha_devolucion and fecha_devolucion.strip():
            messagebox.showerror("Error", "Un préstamo Activo no puede tener fecha de devolución.")
            return
        
        if fecha_devolucion and fecha_devolucion.strip() and estado=="Devuelto":
            try:
                # Convertir fechas para comparación
                prestamo_date=datetime.strptime(fecha_prestamo, "%Y-%m-%d")
                devolucion_date=datetime.strptime(fecha_devolucion, "%Y-%m-%d")
                
                # Validar que la fecha de devolución sea posterior a la fecha de préstamo
                if devolucion_date<prestamo_date:
                    messagebox.showerror("Error", "La fecha de devolución debe ser posterior a la fecha de préstamo.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use AAAA-MM-DD")
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
        conn.close()