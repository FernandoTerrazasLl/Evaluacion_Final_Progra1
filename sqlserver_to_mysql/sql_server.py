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
    print('Error')

cursor_server = conn.cursor()
#cursor.execute("Select * from categoria")
#row = cursor.fetchall()

#for record in row:
 #   print(record)

