#RECORDAR HACERLO MODULAR EL CODIGO (CREAR MULTIPLES ARCHIVOS PY PARA FUNCIONES O CLASES MAS IMPORTANTES)
import pyodbc

server = 'DESKTOP-T8BJL71'  
database = 'BibliotecaUniversitaria'
username = 'DESKTOP-T8BJL71\\user'

try:
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"Trusted_Connection=yes;"
    )
except:
    print('Connection error in sqlserver')

cursor_server = conn.cursor()
