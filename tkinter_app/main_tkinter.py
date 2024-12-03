#RECORDAR HACERLO MODULAR EL CODIGO (CREAR MULTIPLES ARCHIVOS PY PARA FUNCIONES O CLASES MAS IMPORTANTES)
import tkinter as tk
from tkinter import ttk, messsagebox 
import mysql.connector

class BibliotecaApp:
    def _init_(self, root):
        self.root=root
        self.root.title("Gestión de Biblioteca Universitaria")
        self.root.geometry("800x600")
        self.configure_styles()
        self.create_main_menu()

    def configure_styles(self):
        style=ttk.Style()
        
    def connect_database(self):
        try:
            conn=mysql.connector.connect(
                host="localhost",
                user="root",
                password= #insertar contraseña de la conexion
                database="BibliotecaUniversitaria"
            )
            return conn
        except mysql.connector.Error as err:
            messsagebox.showerror("Error", f"Error conectando a MySQL: {err}")
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
            messsagebox.showerror("Error", f"No se pudo recuperar datos de {table_name}: {e}")
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
            messsagebox.showinfo("Exito", f"Registro agregado a {table_name}.")
        except Exception as e:
            messsagebox.showerror("Error", f"No se pudo agregar el registro a {table_name}:{e}")
        finally:
            conn.close()