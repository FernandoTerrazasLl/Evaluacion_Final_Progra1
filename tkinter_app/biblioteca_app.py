import tkinter as tk
from tkinter import ttk, messagebox

class BibliotecaApp:
    def __init__(self, root, db_connection):
        self.root=root
        self.root.title("Gestión de Biblioteca Universitaria")
        self.root.geometry("800x600")
        self.db_connection=db_connection
        self.create_main_menu()
    
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

        values=[value if value.strip() else None for value in values]

        cursor=conn.cursor()
        try:
            placeholders = ", ".join(["%s"] * len(values))
            cursor.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})", values)
            conn.commit()
            messagebox.showinfo("Éxito", f"Registro agregado a {table_name}.")
            self.fetch_data(tree, table_name)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el registro a {table_name}: {e}")
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
            record_id= tree.item(selected_item)["values"][0]
            query=f"DELETE FROM {table_name} WHERE {id_column} = %s"
            cursor.execute(query, (record_id,))
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

        processed_values=[None if value.strip()=="" else value for value in values]

        cursor=conn.cursor()
        try:
            set_clause=", ".join([f"{col}=%s" for col in columns])
            query=f"UPDATE {table_name} SET {set_clause} WHERE {columns[0]}=%s"

            cursor.execute(query, processed_values + [record_id])
            conn.commit()
            messagebox.showinfo("Éxito", f"Registro actualizado en {table_name}.")
            self.fetch_data(tree, table_name)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el registro de {table_name}: {e}")
        finally:
            conn.close()

    def create_action_interface(self, action, table_name, columns, id_column):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"{action.capitalize()} en {table_name}", font=("Arial", 16)).pack(pady=10)

        tree=ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill="both", expand=True, pady=10)

        self.fetch_data(tree, table_name)

        if action=="eliminar":
            delete_button=tk.Button(
                self.root, text="Eliminar",
                command=lambda: self.delete_data(tree, table_name, id_column)
            )
            delete_button.pack(pady=10)

        back_button=tk.Button(self.root, text="Volver", command=lambda: self.create_table_menu(action))
        back_button.pack(pady=10)

        if action=="agregar" or action=="modificar":
            frame=tk.Frame(self.root)
            frame.pack(pady=10)

            entry_widgets={}
            for i, col in enumerate(columns):
                tk.Label(frame, text=col).grid(row=i, column=0, padx=5, pady=2)
                entry=tk.Entry(frame)
                entry.grid(row=i, column=1, padx=5, pady=2)
                entry_widgets[col]=entry

            if action=="agregar":
                def handle_add():
                    values=[entry_widgets[col].get() for col in columns]
                    self.add_data(tree, table_name, columns, values)
                add_button=tk.Button(frame, text="Agregar", command=handle_add)
                add_button.grid(row=len(columns), column=0, pady=10)

            elif action=="modificar":
                def load_selected(event):
                    selected_item=tree.selection()
                    if not selected_item:
                        return
                    values=tree.item(selected_item)["values"]  
                    for i, col in enumerate(columns):
                        entry_widgets[col].delete(0, tk.END)  
                        entry_widgets[col].insert(0, values[i])

                def handle_update():
                    selected_item=tree.selection()
                    if not selected_item:
                        messagebox.showerror("Error", "Selecciona un registro para modificar.")
                        return
                    record_id=tree.item(selected_item)["values"][0]
                    values=[entry_widgets[col].get() for col in columns]
                    self.update_data(tree, table_name, columns, values, record_id)

                tree.bind("<ButtonRelease-1>", load_selected)

                update_button=tk.Button(frame, text="Modificar", command=handle_update)
                update_button.grid(row=len(columns), column=1, pady=10)

    def create_table_menu(self, action):
        for widget in self.root.winfo_children():
            widget.destroy()

        tables={
            "Usuario": ["usuario_id", "nombre", "apellido", "correo", "tipo_usuario","carrera", "fecha_registro", "fecha_modificacion"],
            "Bibliotecario": ["bibliotecario_id", "nombre", "apellido", "fecha_contratacion", "correo", "fecha_despido", "fecha_modificacion"],
            "Prestamo": ["prestamo_id", "usuario_id", "fecha_prestamo", "fecha_devolucion", "estado", "fecha_limite_devolucion", "bibliotecario_id", "fecha_modificacion"],
            "Detalle_Prestamo": ["detalle_id", "prestamo_id", "libro_id", "cantidad", "fecha_modificacion"],
            "Libro": ["libro_id", "titulo", "anio_publicacion", "editorial", "tipo_texto_id", "categoria_id",
                      "copias_totales", "fecha_modificacion"],
            "Autor": ["autor_id", "nombre", "apellido", "fecha_modificacion"],
            "Libro_Autor": ["libro_id", "autor_id", "fecha_modificacion"],
            "Categoria": ["categoria_id", "nombre_categoria", "fecha_modificacion"],
            "Tipo_Texto": ["tipo_texto_id", "nombre_tipo", "fecha_modificacion"]
        }

        for table_name, columns in tables.items():
            tk.Button(
                self.root,
                text=table_name,
                width=20,
                command=lambda t=table_name, c=columns: self.create_action_interface(action, t, c, c[0])
            ).pack(pady=5)

        back_button=tk.Button(self.root, text="Volver", command=self.create_main_menu)
        back_button.pack(pady=10)

    def create_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Sistema de Gestión de Biblioteca Universitaria", font=("Arial", 20)).pack(pady=20)

        actions=["visualizar", "agregar", "modificar", "eliminar"]
        for action in actions:
            tk.Button(
                self.root,
                text=action.capitalize(),
                width=20,
                command=lambda a=action: self.create_table_menu(a)
            ).pack(pady=5)