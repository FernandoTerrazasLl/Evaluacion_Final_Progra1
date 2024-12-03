#RECORDAR HACERLO MODULAR EL CODIGO (CREAR MULTIPLES ARCHIVOS PY PARA FUNCIONES O CLASES MAS IMPORTANTES)
import tkinter as tk
from tkinter import ttk, messsagebox 

class App:
    def _init_(self, root):
        self.root=root
        self.root.title("Gestión de Biblioteca Universitaria")
        #insertar conexion a db

        self.create_widgets()

    def create_widgets(self):
        self.tree=ttk.Treeview(self.root, columns=("ID", "Nombre", "Autor"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Autor", text="Autor")
        self.tree.pack(fill=tk.BOTH, expand=True)
    

    def load_records(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
    def add_records(self):
        self.record_form("Agregar Registro")
    
    def edit_record(self):
        selected_item=self.tree.selection()

    