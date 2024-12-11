from tkinter import messagebox 
import mysql.connector
import pyodbc
from dataclasses import dataclass

@dataclass
class DatabaseConnection:
    db_type:str
    connection_params:dict

    def connect(self):
        try:
            if self.db_type=="mysql":
                conn=mysql.connector.connect(**self.connection_params)
            elif self.db_type=="sqlserver":
                conn=pyodbc.connect(
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={self.connection_params['server']};"
                    f"DATABASE={self.connection_params['database']};"
                    f"Trusted_Connection={self.connection_params.get('trusted_connection', 'yes')};"
                )
            else:
                raise ValueError("Tipo de base de datos no soportado.")
            return conn
        except Exception as e:
            messagebox.showerror("Error", f"Error conectando a la base de datos: {e}")
            return None
        