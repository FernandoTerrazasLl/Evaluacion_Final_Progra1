import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from funciones import fetch_data, add_data, delete_data, update_data

class BibliotecaApp:
    def __init__(self, root, db_connection):
        self.root=root
        self.root.title("Gestión de Biblioteca Universitaria")
        self.root.geometry("800x600")
        self.db_connection=db_connection
        self.create_main_menu()

    def create_action_interface(self, action, table_name, columns, id_column):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text=f"{action.capitalize()} en {table_name}", font=("Arial", 16)).pack(pady=10)
        tree=ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill="both", expand=True, pady=10)
        fetch_data(self.db_connection, tree, table_name)

        form_columns=columns[1:]

        if table_name== "prestamo":
            if action in ["agregar", "modificar"]:
                self.create_prestamo_form(action, tree, table_name, form_columns)
            elif action == "eliminar":
                delete_button = tk.Button(
                    self.root, text="Eliminar",
                    command=lambda: delete_data(self.db_connection, tree, table_name, id_column)
                )
                delete_button.pack(pady=10)

        else:
            if action=="eliminar":
                delete_button=tk.Button(
                    self.root, text="Eliminar",
                    command=lambda: delete_data(self.db_connection, tree, table_name, id_column)
                )
                delete_button.pack(pady=10)
            if action in ["agregar", "modificar"]:
                self.create_form(action, tree, table_name, form_columns, id_column)

        back_button=tk.Button(self.root, text="Volver", command=lambda: self.create_table_menu(action))
        back_button.pack(pady=10)

    def create_prestamo_form(self, action, tree, table_name, form_columns):
        frame=tk.Frame(self.root)
        frame.pack(pady=10)
        form_columns=[col for col in form_columns if col!='fecha_modificacion']

        entry_widgets={}
        for i, col in enumerate(form_columns):
            if col=="estado":
                tk.Label(frame, text=col).grid(row=i, column=0, padx=5, pady=2)
                estado_var=tk.StringVar()
                estado_frame=tk.Frame(frame)
                estado_frame.grid(row=i, column=1, padx=5, pady=2)

                def update_estado_fields(*args):
                    estado=estado_var.get()
                    if estado=="Activo":
                        entry_widgets["fecha_devolucion"].delete(0, tk.END)
                        entry_widgets["fecha_devolucion"].config(state="disabled")
                    else:
                        entry_widgets["fecha_devolucion"].config(state="normal")

                tk.Radiobutton(estado_frame, text="Activo", variable=estado_var, value="Activo", command=update_estado_fields).pack(side="left")
                tk.Radiobutton(estado_frame, text="Devuelto", variable=estado_var, value="Devuelto", command=update_estado_fields).pack(side="left")
                estado_var.trace_add("write", update_estado_fields)
                entry_widgets[col]=estado_var
            else:
                tk.Label(frame, text=col).grid(row=i, column=0, padx=5, pady=2)
                entry=tk.Entry(frame)
                entry.grid(row=i, column=1, padx=5, pady=2)
                entry_widgets[col] = entry

                # Mensaje formato fecha
                if "fecha" in col.lower():
                    tk.Label(frame, text="AAAA-MM-DD", fg="gray").grid(row=i, column=2, padx=5, pady=2)

        def handle_add():
            values = []
            for col in form_columns:
                if col == "estado":
                    values.append(entry_widgets[col].get())
                else:
                    values.append(entry_widgets[col].get())

            # Validar fechas
            try:
                fecha_prestamo = datetime.strptime(entry_widgets['fecha_prestamo'].get(), "%Y-%m-%d")
                fecha_devolucion = datetime.strptime(entry_widgets['fecha_devolucion'].get(), "%Y-%m-%d")
                fecha_limite_devolucion = datetime.strptime(entry_widgets['fecha_limite_devolucion'].get(), "%Y-%m-%d")

                if fecha_prestamo >= fecha_devolucion:
                    messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha de devolución.")
                    return
                if fecha_prestamo >= fecha_limite_devolucion:
                    messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha límite de devolución.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use AAAA-MM-DD.")
                return

            # Agregar datos a la tabla
            add_data(self.db_connection, tree, table_name, form_columns, values)

        def handle_update():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Selecciona un registro para modificar.")
                return

            record_id = tree.item(selected_item)["values"][0]
            values = []
            for col in form_columns:
                if col == "estado":
                    values.append(entry_widgets[col].get())
                else:
                    values.append(entry_widgets[col].get())

            # Validar fechas
            try:
                fecha_prestamo = datetime.strptime(entry_widgets['fecha_prestamo'].get(), "%Y-%m-%d")
                fecha_devolucion = datetime.strptime(entry_widgets['fecha_devolucion'].get(), "%Y-%m-%d")
                fecha_limite_devolucion = datetime.strptime(entry_widgets['fecha_limite_devolucion'].get(), "%Y-%m-%d")

                if fecha_prestamo>fecha_devolucion:
                    messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha de devolución.")
                    return
                if fecha_prestamo>fecha_limite_devolucion:
                    messagebox.showerror("Error", "La fecha de préstamo debe ser menor que la fecha límite de devolución.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use AAAA-MM-DD.")
                return
            update_data(self.db_connection, tree, table_name, form_columns, values, record_id)

        if action=="agregar":
            tk.Button(frame, text="Agregar", command=handle_add).grid(row=len(form_columns), column=0, pady=10)
        elif action=="modificar":
            def load_selected(event):
                selected_item=tree.selection()
                if not selected_item:
                    return
                values=tree.item(selected_item)["values"]
                for i, col in enumerate(form_columns):
                    if col=="estado":
                        entry_widgets[col].set(values[i+1])
                    else:
                        entry_widgets[col].delete(0, tk.END)
                        entry_widgets[col].insert(0, values[i+1])

            tree.bind("<ButtonRelease-1>", load_selected)
            tk.Button(frame, text="Modificar", command=handle_update).grid(row=len(form_columns), column=0, pady=10)

    def create_form(self, action, tree, table_name, columns, id_column):
        form_columns=[col for col in columns if col!='fecha_modificacion']
        frame=tk.Frame(self.root)
        frame.pack(pady=10)

        entry_widgets={}
        for i, col in enumerate(form_columns):
            tk.Label(frame, text=col).grid(row=i, column=0, padx=5, pady=2)
            entry=tk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=2)
            entry_widgets[col]=entry

            # Mensaje formato fecha
            if "fecha" in col.lower():
                tk.Label(frame, text="AAAA-MM-DD", fg="gray").grid(row=i, column=2, padx=5, pady=2)

        if action=="agregar":
            def handle_add():
                values=[entry_widgets[col].get() for col in form_columns]
                add_data(self.db_connection, tree, table_name, form_columns, values)
            tk.Button(frame, text="Agregar", command=handle_add).grid(row=len(form_columns), column=0, pady=10)

        elif action=="modificar":
            def load_selected(event):
                selected_item=tree.selection()
                if not selected_item:
                    return
                values=tree.item(selected_item)["values"]
                for i, col in enumerate(form_columns):
                    entry_widgets[col].delete(0, tk.END)
                    entry_widgets[col].insert(0, values[i+1])

            def handle_update():
                selected_item=tree.selection()
                if not selected_item:
                    messagebox.showerror("Error", "Selecciona un registro para modificar.")
                    return
                record_id=tree.item(selected_item)["values"][0]
                values=[entry_widgets[col].get() for col in form_columns]
                update_data(self.db_connection, tree, table_name, form_columns, values, record_id)
            tree.bind("<ButtonRelease-1>", load_selected)
            tk.Button(frame, text="Modificar", command=handle_update).grid(row=len(form_columns), column=0, pady=10)
    
    def obtener_tablas_y_columnas(self):
        if not self.db_connection.mydb or not self.db_connection.mydb.is_connected():
            print("Reconectando a MySQL...")
            self.db_connection.conectar_mysql()

        conn=self.db_connection.mydb
        cursor=conn.cursor()
        cursor.execute("SHOW TABLES;")
        tablas=cursor.fetchall()

        tablas_columnas={}
        for tabla in tablas:
            tabla_nombre=tabla[0]
            cursor.execute(f"DESCRIBE {tabla_nombre};")
            columnas=[col[0] for col in cursor.fetchall()]
            tablas_columnas[tabla_nombre]=columnas

        return tablas_columnas

    def create_table_menu(self, action):
        for widget in self.root.winfo_children():
            widget.destroy()

        tablas_columnas=self.obtener_tablas_y_columnas()

        for table_name, columns in tablas_columnas.items():
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