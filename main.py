from io_handler import cargar_recursos, cargar_trabajo, tiempo_cronograma, tabla_cronograma
#porueba para ver solo el cronograma
def main():
    ruta_recursos = "data/resources-e01a.json" 
    ruta_trabajo = "data/works-e01b.json"
    recursos = cargar_recursos(ruta_recursos)
    trabajo = cargar_trabajo(ruta_trabajo)
    resultado = tiempo_cronograma(trabajo, recursos)
    tabla_cronograma(resultado)
if __name__ == "__main__":
    main()
#------------------------------------------------------------------------------------------------