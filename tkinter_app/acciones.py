from tkinter import messagebox

def fetch_data(self, tree, table_name):
    conn=self.db_connection.connect()
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

def add_data(self, tree, table_name, columns, values):
    conn=self.db_connection.connect()
    if not conn: 
        return
    
    cursor=conn.cursor()
    try:
        placeholders=", ".join(["%s"]*len(values))
        cursor.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})", values)
        conn.commit()
        messagebox.showinfo("Exito", f"Registro agregado a {table_name}.")
        self.fetch_data(tree, table_name)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el registro a {table_name}:{e}")
    finally:
        conn.close()

def delete_data(self, tree, table_name, id_column):
    selected_item=tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Selecciona un registro para eliminar.")
        return

    conn=self.db_connection.connect()
    if not conn:
        return

    cursor=conn.cursor()
    try:
        record_id=tree.item(selected_item)["values"][0]
        cursor.execute(f"DELETE FROM {table_name} WHERE {id_column} = %s", (record_id,))
        conn.commit()
        messagebox.showinfo("Éxito", f"Registro eliminado de {table_name}.")
        self.fetch_data(tree, table_name)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el registro de {table_name}: {e}")
    finally:
        conn.close()

def update_data(self, tree, table_name, columns, values, record_id):
    conn=self.db_connection.connect()
    if not conn:
        return
    
    cursor=conn.cursor()
    try:
        set_clause=", ".join([f"{col}=%s" for col in columns])
        cursor.execute(
            f"UPDATE {table_name} SET {set_clause} WHERE {columns[0]}=%s",
            values+[record_id]
        )
        conn.commit()
        messagebox.showinfo("Éxito", f"Registro actualizado en {table_name}.")
        self.fetch_data(tree, table_name)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el registro de {table_name}: {e}")
    finally:
        conn.close()