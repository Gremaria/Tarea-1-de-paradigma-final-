from typing import List, Dict, Any

# 1. Función de utilidad para compatibilidad
def es_compatible(recurso: Dict, tarea: Dict) -> bool:
    return tarea["category"] in recurso["categories"]

# 2. Función núcleo del cronograma
def calcular_cronograma(tareas: List[Dict], recursos: List[Dict]) -> List[Dict]:
    cronograma = []
    # Estado inicial: todos los recursos libres en tiempo 0
    liberacion_recursos = {r["id"]: 0.0 for r in recursos}
    
    # Ordenar por urgencia (deadline)
    tareas_ordenadas = sorted(tareas, key=lambda x: x["deadline"])

    for tarea in tareas_ordenadas:
        asignada = False
        for recurso in recursos:
            if es_compatible(recurso, tarea):
                id_res = recurso["id"]
                
                # Tiempo de inicio (considerando disponibilidad del recurso)
                inicio = liberacion_recursos[id_res]
                
                # Cálculo según eficiencia (ej: span 4 / ef 1 = 4 unidades de tiempo)
                duracion = tarea["span"] / recurso["efficiency"]
                fin = inicio + duracion
                
                # Guardar resultado
                cronograma.append({
                    "task": tarea["id"],
                    "resource": id_res,
                    "start": round(inicio, 2),
                    "end": round(fin, 2)
                })
                
                # Actualizar estado para la siguiente asignación
                liberacion_recursos[id_res] = fin
                asignada = True
                break # Salir del loop de recursos para ir a la siguiente tarea
                
    return cronograma