from tkinter import messagebox

#Visualizar Datos
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

#Añadir datos
def add_data(db_connection, tree, table_name, columns, values):
    conn=db_connection.connect()
    if not conn:
        return
    values=[value if value.strip() else None for value in values]
    cursor=conn.cursor()
    try:
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

#Eliminar datos
def delete_data(db_connection, tree, table_name, id_column):
    selected_item=tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Selecciona un registro para eliminar.")
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

#Modificar datos
def update_data(db_connection, tree, table_name, columns, values, record_id):
    conn=db_connection.connect()
    if not conn:
        return
    processed_values=[None if value.strip()=="" else value for value in values]
    cursor=conn.cursor()
    try:
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
