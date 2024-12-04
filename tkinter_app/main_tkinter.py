#RECORDAR HACERLO MODULAR EL CODIGO (CREAR MULTIPLES ARCHIVOS PY PARA FUNCIONES O CLASES MAS IMPORTANTES)
#RECORDAR HACERLO MODULAR EL CODIGO (CREAR MULTIPLES ARCHIVOS PY PARA FUNCIONES O CLASES MAS IMPORTANTES)
import tkinter as tk
from tkinter import ttk, messagebox 
import mysql.connector

class BibliotecaApp:
    def __init__(self, root):
        self.root=root
        self.root.title("Gestión de Biblioteca Universitaria")
        self.root.geometry("800x600")
        self.create_main_menu()
        
    def connect_database(self):
        try:
            conn=mysql.connector.connect(
                host="localhost",
                user="root",
                password= "#insertar contraseña de la conexion",
                database="BibliotecaUniversitaria"
            )
            return conn
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error conectando a MySQL: {err}")
            return None
    
    def fetch_data(self, tree, table_name):
        conn=self.connect_database()
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
        conn=self.connect_database()
        if not conn: 
            return
        
        cursor=conn.cursor()
        try:
            placeholders=", ".join(["%s"] * len(values))
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

        conn=self.connect_database()
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

        if action=="agregar":
            frame=tk.Frame(self.root)
            frame.pack(pady=10)

            entry_widgets={}
            for i, col in enumerate(columns[1:]):  # Excluir ID en la entrada
                tk.Label(frame, text=col).grid(row=i, column=0, padx=5, pady=2)
                entry=tk.Entry(frame)
                entry.grid(row=i, column=1, padx=5, pady=2)
                entry_widgets[col]=entry

            def handle_add():
                values=[entry.get() for entry in entry_widgets.values()]
                self.add_data(tree, table_name, columns[1:], values)

            add_button = tk.Button(frame, text="Agregar", command=handle_add)
            add_button.grid(row=len(columns), column=0, pady=10)

        elif action=="eliminar":
            delete_button = tk.Button(self.root, text="Eliminar",
                                      command=lambda: self.delete_data(tree, table_name, id_column))
            delete_button.pack(pady=10)

        back_button=tk.Button(self.root, text="Volver", command=lambda: self.create_table_menu(action))
        back_button.pack(pady=10)
