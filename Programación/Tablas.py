import sqlite3

base = "Base_fabrica.db"

con = sqlite3.connect(base)
cursor = con.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        cantidad INTEGER NOT NULL,
        defectuosas INTEGER NOT NULL,
        fecha_entrada TEXT NOT NULL)
               """)
cursor.close()
con.close()