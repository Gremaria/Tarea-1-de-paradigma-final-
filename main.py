from io_handler import cargar_trabajo, cargar_recursos, tiempo_cronograma, tabla_cronograma

def main():
    # 1. Pedir archivos
    tareas_path = input("Archivo de tareas: ")
    recursos_path = input("Archivo de recursos: ")

    # 2. Cargar datos
    tareas = cargar_trabajo(tareas_path)
    recursos = cargar_recursos(recursos_path)

    # 3. Generar cronograma
    resultado = tiempo_cronograma(tareas, recursos)

    # 4. Mostrar resultados
    print("\nTiempo de ejecución:", resultado["tiempo_ms"], "segundos")

    # 5. Mostrar tabla bonita
    tabla_cronograma(resultado)


if __name__ == "__main__":
    main()