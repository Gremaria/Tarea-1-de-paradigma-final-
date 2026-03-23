from io_handler import cargar_trabajo, cargar_recursos, tiempo_cronograma, tabla_cronograma
from scheduler import tiempos_cronograma, compatibilidad
import json
def main():

    tareas_path = input("Archivo de tareas: ")
    recursos_path = input("Archivo de recursos: ")

    tareas = cargar_trabajo(tareas_path)
    recursos = cargar_recursos(recursos_path)
    print("hoalnsdaksndkan")
    resultado = tiempos_cronograma(recursos, tareas)

    print("\nTiempo de ejecución:", resultado["tiempo_ms"], "segundos")

    tabla_cronograma(resultado)
    opcion = input("\n¿Guardar cronograma? (s/n): ")

    if opcion.lower() == "s":
        nombre = input("Nombre del archivo (ej: output.json): ")
    
        with open(nombre, "w") as f:
            json.dump(resultado["lista"], f, indent=4)
    
        print(f"Cronograma guardado en {nombre}")

if __name__ == "__main__":
    main()