from io_handler import  tabla_cronograma
from scheduler import cargar_trabajo, cargar_recursos, tiempos_minimizados, tiempo_retraso_minimizado, compatibilidad, cantidad_atrasos_minimizada
import json

def main():
    # 1. Pedir archivos
    tareas_path = input("Archivo de tareas: ")
    recursos_path = input("Archivo de recursos: ")

    # 2. Cargar datos
    tareas = cargar_trabajo(tareas_path)
    recursos = cargar_recursos(recursos_path)



    # 3. Generar cronograma
    
    print("\n Ingrese 1 si desea minimizar el tiempo total, 2 si desea minimizar el tiempo de retraso, o 3 si desea minimizar la cantidad de tareas atrasadas")
    opcion = input()
    
    if opcion == "1":
        resultado = tiempos_minimizados(recursos, tareas)
    elif opcion == "2":
        resultado = tiempo_retraso_minimizado(recursos, tareas)
    elif opcion == "3":
        resultado = cantidad_atrasos_minimizada(recursos, tareas)
    else:
        print("Respuesta inválida")
        return
    # 4. Mostrar resultados
    print("\nTiempo de ejecución:", resultado["tiempo_ms"], "ms")

    # 5. Mostrar tabla bonita
    tabla_cronograma(resultado)

    guardar = input("\n¿Guardar cronograma? (s/n): ").strip().lower()
    if guardar == "s":
        nombre = input("Nombre archivo salida: ").strip()

        salida = []
        for c in resultado["lista"]:
            salida.append({
                "work": c["id"],
                "resource": c["recurso"],
                "start": c["inicio"],
                "end": c["fin"]
            })

    with open(nombre, "w") as f:
        json.dump(salida, f, indent=4)

    print("Cronograma guardado.")



if __name__ == "__main__":
    main()