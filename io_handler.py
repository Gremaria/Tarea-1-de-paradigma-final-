import json 
from typing import List, Dict, Any 
import time
from rich.table import Table
from rich.console import Console
 
#datos de json 



print("-------------------------------------------------------------------------------------------------------------------------------------------")

def tiempos_minimizados (trabajo:List, recursos: List)-> Dict:
     ejecucion=time.time() 
     cronograma= []  # donde se agrega los datos para el cronograma 
     recursos_libre={r["id"]: 0 for r in recursos} #[:10]
     cantidad_por_recurso= {r["id"]: 0 for r in recursos} #[:10]
     for t in trabajo: 
        for r in recursos: 
           if  t["category"]in r["categories"]:
            duracion = t["span"] / r["efficiency"]
            comienzo =recursos_libre [r["id"]]
            fin = comienzo + duracion
            retraso= max(0.0, fin - t["deadline"])
            cumple = fin <= t["deadline"]

            cronograma.append({"id" : t["id"],"recurso" :r["id"],"inicio": comienzo,"fin": fin,"retraso": retraso,"cumple": cumple})
            
        
            recursos_libre[r["id"]]=fin 
            cantidad_por_recurso[r["id"]]+= duracion 
            break 
     fin_ejecucion= time. time()
     ejecucion_total= (fin_ejecucion - ejecucion)
     return {"lista": cronograma, "tiempo_ms": ejecucion_total,"uso_recursos": cantidad_por_recurso}






print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------")        
                
# generador de tabla con rich
def tabla_cronograma (datos_cronograma:Dict):
    console= Console()
    cronograma = datos_cronograma["lista"]
    tabla= Table(title= "cronograma")
    tabla.add_column("tarea")
    tabla.add_column("recurso")
    tabla. add_column("inicio")
    tabla. add_column("fin")
    tabla. add_column("retraso")
    tabla. add_column("cumple")
   
    for c in cronograma:
        status= "True" if c["cumple"] else "False"
        tabla.add_row(c["id"],c["recurso"],f"{c['inicio']:.2f}",f"{c['fin']:.2f}",f"{c['retraso']:.2f}",status)
    console.print(tabla)
    retrasos_totales= sum (c["retraso"] for c in cronograma)
    tareas_cumplidas= sum(c["cumple"] for c in cronograma)

    duracion_total = max(c["fin"] for c in cronograma)
    
    porcentaje = (tareas_cumplidas / len(cronograma)) * 100
    console.print("\nEstadisticas Finales:")
    console.print(f" Makespan: {duracion_total:.2f}")
    console.print(f" Suma de Retrasos: {retrasos_totales:.2f}")
    console.print(f" Cumplimiento Deadlines: {porcentaje:.1f}%")
    console.print("\nUso por Recurso")
    for rid, tiempo_uso in datos_cronograma["uso_recursos"].items():
       
        porc_uso = (tiempo_uso / duracion_total) * 100
        console.print(f"{rid}: {porc_uso:.1f}% ")
    






            


















    
                


















