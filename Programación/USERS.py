import csv
import os
from datetime import datetime
import pandas as pd
import sqlite3

# Archivo CSV donde se guardarán los datos
ARCHIVO_CSV = 'inventario_componentes.csv'

# Crear archivo CSV si no existe 
def inicializar_csv():
    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Nombre', 'Cantidad', 'Defectuosas', 'Fecha_Entrada'])

# Añadir componente
def añadir_componente(nombre, cantidad):
    with open(ARCHIVO_CSV, 'r', encoding='utf-8') as f:
        lineas = list(csv.reader(f))
    
    # Buscar si ya existe el componente
    encontrado = False
    for i, fila in enumerate(lineas[1:], start=1):
        if fila[1].lower() == nombre.lower():
            lineas[i][2] = str(int(fila[2]) + cantidad)
            encontrado = True
            break
    
    if not encontrado:
        nuevo_id = len(lineas)
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M')
        lineas.append([nuevo_id, nombre, cantidad, 0, fecha])
    
    with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(lineas)
    
    print(f" Componente '{nombre}' añadido: {cantidad} unidades")

# Marcar piezas defectuosas
# Hemos usado la ia para crear este bucle y con ayuda de Filip

def marcar_defectuosas(nombre, cantidad_defectuosa):
    with open(ARCHIVO_CSV, 'r', encoding='utf-8') as f:
        lineas = list(csv.reader(f))
    
    encontrado = False
    for i, fila in enumerate(lineas[1:], start=1):
        if fila[1].lower() == nombre.lower():
            lineas[i][3] = str(int(fila[3]) + cantidad_defectuosa)
            encontrado = True
            print(f" Marcadas {cantidad_defectuosa} unidades defectuosas de '{nombre}'")
            break
    
    if not encontrado:
        print(f" Componente '{nombre}' no encontrado")
        return
    
    with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(lineas)

# Hasta hemos usado la ia

# Consultar inventario
def consultar_inventario():
    print("\n" + "="*70)
    print("INVENTARIO ACTUAL")
    print("="*70)
    
    with open(ARCHIVO_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  
        
        for fila in reader:
            id_comp, nombre, cantidad, defectuosas, fecha = fila
            buenas = int(cantidad) - int(defectuosas)
            print(f"ID: {id_comp} | {nombre}")
            print(f"  Total: {cantidad} | Buenas: {buenas} | Defectuosas: {defectuosas}")
            print(f"  Fecha entrada: {fecha}")
            print("-"*70)

def eliminar_piezas(id_pieza_a_eliminar):
    df = pd.read_csv(ARCHIVO_CSV)
    if id_pieza_a_eliminar not in df ["ID"].values:
        print(f"ID {id} no encontrado.")
        id = int(input("dame otro id: "))
    else:
        df_eliminado = df[df["ID"] != id_pieza_a_eliminar]
        df_eliminado.to_csv(ARCHIVO_CSV, index=False)
        print(f"Pieza con el id {id_pieza_a_eliminar}, Eliminado. ")

def guardar():
    con = sqlite3.connect("Base_fabrica.db")
    df = pd.read_csv(ARCHIVO_CSV)
    df.to_sql("inventario", con, if_exists='replace', index=False)
    con.close()

    pass

#  Menú principal
def menu():
    inicializar_csv()
    
    while True:
        print("\n" + "="*50)
        print("SISTEMA DE GESTIÓN DE COMPONENTES")
        print("="*50)
        print("1. Añadir componente")
        print("2. Marcar piezas defectuosas")
        print("3. Consultar inventario")
        print("4. Eliminar piezas")
        print("5. Salir")
        
        opcion = input("\nElige una opción: ")
        
        match opcion:
            case "1":
                nombre = input("Nombre del componente: ")
                cantidad = int(input("Cantidad: "))
                añadir_componente(nombre, cantidad)
        
            case "2":
                nombre = input("Nombre del componente: ")
                cantidad = int(input("Cantidad defectuosa: "))
                marcar_defectuosas(nombre, cantidad)
         
            case "3":
                consultar_inventario()

            case "4":
                id = int(input("Dame el id: "))
                eliminar_piezas(id)
        
            case "5":
                guardar()
                print("\n Saliendo del sistema...")
                break
            case _:
                print("opcion no valida!")


# Ejecutar programa
if __name__ == "__main__":
    menu()