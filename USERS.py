import csv
import os
from datetime import datetime

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
# Hemos usado la ia en este bucle porque no conseguiamos que funcionase bien y la ia nos a ayudado a entenderlo y que ejecute.

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

# Hasta aqui lo hemos usado.

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
        print("4. Salir")
        
        opcion = input("\nElige una opción: ")
        
        if opcion == '1':
            nombre = input("Nombre del componente: ")
            cantidad = int(input("Cantidad: "))
            añadir_componente(nombre, cantidad)
        
        elif opcion == '2':
            nombre = input("Nombre del componente: ")
            cantidad = int(input("Cantidad defectuosa: "))
            marcar_defectuosas(nombre, cantidad)
        
        elif opcion == '3':
            consultar_inventario()
        
        elif opcion == '4':
            print("\n Saliendo del sistema...")
            break
        
        else:
            print(" Opción no válida")

# Ejecutar programa
if __name__ == "__main__":
    menu()