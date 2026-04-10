from typing import List, Dict, Any 
import json
import time
#datos de json 

def cargar_recursos(ruta: str):
    with open(ruta, "r") as f:
        return json.load(f)

def cargar_trabajo(ruta: str):
    with open(ruta, "r") as f:
        return json.load(f)


# Funcion para evaluar si existe una categoria del trabajo en un recurso dado
def compatibilidad(recursos:Dict,trabajo:Dict)->bool: 
    return trabajo["category"] in recursos["categories"]


def tiempos_minimizados(recursos: Dict, trabajos: Dict) -> dict:

    ejecucion=time.time()


    # se ordena el diccionario de trabajos de mayor a menor
    trabajos = sorted(trabajos, key=lambda x: x["span"], reverse=True)
    recursos = sorted(recursos, key=lambda x: x["efficiency"], reverse=True)

    flag_recurso = {}  # variable que representa si un recurso es compatible con el trabajo siendo loopeado
    cronograma= []  # donde se agrega los datos para el cronograma 
    recursos_libre={r["id"]: 0 for r in recursos}
    cantidad_por_recurso= {r["id"]: 0 for r in recursos}

    for recurso in recursos:
        flag_recurso[recurso["id"]] = False

    for trabajo in trabajos:
        menor = 10000 #valor arbitrario grande

        for recurso in recursos:
            flag_recurso[recurso["id"]] = compatibilidad(recurso, trabajo)
            duracion = trabajo["span"] / recurso["efficiency"]

            if (flag_recurso[recurso["id"]] == True) and (recursos_libre[recurso["id"]] + duracion <= menor):
                menor = recursos_libre[recurso["id"]] + duracion - 1
                #si los valores son compatibles y el tiempo de finalizacion de uso del recurso es menor al menor valor registrado,
                #se reemplaza el menor valor con el del recurso menos 1, ya que empates son irrelevantes
            else:
                flag_recurso[recurso["id"]] = False
                #se reinicia a falso, necesario si hay compatibilidad pero el tiempo es mayor al menor establecido

        for recurso in reversed(recursos): #se usa la lista al revés, ya que el último valor marcado como True es el relevante
            if flag_recurso[recurso["id"]] == True:
                duracion = trabajo["span"] / recurso["efficiency"]
                comienzo =recursos_libre [recurso["id"]]
                fin = comienzo + duracion
                retraso = max(0.0, fin - trabajo["deadline"])
                cumple = fin <= trabajo["deadline"]
                recursos_libre[recurso["id"]]=fin

                cronograma.append({"id" : trabajo["id"],"recurso" :recurso["id"],"inicio": comienzo,"fin": fin,"retraso": retraso,"cumple": cumple})
                cantidad_por_recurso[recurso["id"]]+= duracion 
                break
            flag_recurso[recurso["id"]] = False #se reinician todas las posibles compatibilidades a False



    fin_ejecucion= time. time()
    ejecucion_total= (fin_ejecucion - ejecucion)

    return {"lista": cronograma, "tiempo_ms": ejecucion_total,"uso_recursos": cantidad_por_recurso}


def tiempo_retraso_minimizado(recursos: Dict, trabajos: Dict) -> dict:

    ejecucion=time.time()*1000


    # se ordena el diccionario de trabajos de mayor a menor
    trabajos = sorted(trabajos, key=lambda x: x["deadline"], reverse=False)
    recursos = sorted(recursos, key=lambda x: x["efficiency"], reverse=False)

    flag_recurso = {}  # variable que representa si un recurso es compatible con el trabajo siendo loopeado
    cronograma= []  # donde se agrega los datos para el cronograma 
    recursos_libre={r["id"]: 0 for r in recursos}
    cantidad_por_recurso= {r["id"]: 0 for r in recursos}

    for recurso in recursos:
        flag_recurso[recurso["id"]] = False

    for trabajo in trabajos:
        menor = 10000 #valor arbitrario grande

        for recurso in recursos:
            flag_recurso[recurso["id"]] = compatibilidad(recurso, trabajo)

            if flag_recurso[recurso["id"]] == True:
                fin_estimado = recursos_libre[recurso["id"]] + (trabajo["span"] / recurso["efficiency"])

                if fin_estimado < menor:
                    menor = fin_estimado
                else:
                    flag_recurso[recurso["id"]] = False

            else:
                flag_recurso[recurso["id"]] = False
                #se reinicia a falso, necesario si hay compatibilidad pero el tiempo es mayor al menor establecido

        for recurso in reversed(recursos): #se usa la lista al revés, ya que el último valor marcado como True es el relevante
            if flag_recurso[recurso["id"]] == True:
                duracion = trabajo["span"] / recurso["efficiency"]
                comienzo =recursos_libre [recurso["id"]]
                fin = comienzo + duracion
                retraso = max(0.0, fin - trabajo["deadline"])
                cumple = fin <= trabajo["deadline"]
                recursos_libre[recurso["id"]]=fin

                cronograma.append({"id" : trabajo["id"],"recurso" :recurso["id"],"inicio": comienzo,"fin": fin,"retraso": retraso,"cumple": cumple})
                cantidad_por_recurso[recurso["id"]]+= duracion 
                break
            flag_recurso[recurso["id"]] = False #se reinician todas las posibles compatibilidades a False



    fin_ejecucion= time. time()
    ejecucion_total= (fin_ejecucion - ejecucion)

    return {"lista": cronograma, "tiempo_ms": ejecucion_total,"uso_recursos": cantidad_por_recurso}



def cantidad_atrasos_minimizada(recursos: Dict, trabajos: Dict) -> dict:

    ejecucion = time.time()

    trabajos = sorted(trabajos, key=lambda x: x["deadline"], reverse=False)
    recursos = sorted(recursos, key=lambda x: x["efficiency"], reverse=False)

    flag_recurso = {}  # variable que representa si un recurso es compatible con el trabajo siendo loopeado
    cronograma = []  # donde se agrega los datos para el cronograma
    recursos_libre = {r["id"]: 0 for r in recursos}
    cantidad_por_recurso = {r["id"]: 0 for r in recursos}
    pendientes = [] #trabajos que no pueden cumplir su deadline

    for recurso in recursos:
        flag_recurso[recurso["id"]] = False

    for trabajo in trabajos:
        menor = 10000
        puede_cumplir = False  #flag para saber si algún recurso cumple el deadline

        for recurso in recursos:
            flag_recurso[recurso["id"]] = compatibilidad(recurso, trabajo)

            if flag_recurso[recurso["id"]] == True:
                fin_estimado = recursos_libre[recurso["id"]] + (trabajo["span"] / recurso["efficiency"])

                #solo se considera el recurso si cumple el deadline
                if fin_estimado <= trabajo["deadline"] and fin_estimado < menor:
                    menor = fin_estimado
                    puede_cumplir = True
                else:
                    flag_recurso[recurso["id"]] = False

            else:
                flag_recurso[recurso["id"]] = False

        #si ningún recurso cumple el deadline, se guarda como pendiente
        if not puede_cumplir:
            pendientes.append(trabajo)
            continue

        for recurso in reversed(recursos):
            if flag_recurso[recurso["id"]] == True:
                duracion = trabajo["span"] / recurso["efficiency"]
                comienzo = recursos_libre[recurso["id"]]
                fin = comienzo + duracion
                retraso = max(0.0, fin - trabajo["deadline"])
                cumple = fin <= trabajo["deadline"]
                recursos_libre[recurso["id"]] = fin

                cronograma.append({"id": trabajo["id"], "recurso": recurso["id"], "inicio": comienzo, "fin": fin, "retraso": retraso, "cumple": cumple})
                cantidad_por_recurso[recurso["id"]] += duracion
                break
            flag_recurso[recurso["id"]] = False

    #se asignan los pendientes al recurso compatible con menor carga
    for trabajo in pendientes:
        menor = 10000

        for recurso in recursos:
            flag_recurso[recurso["id"]] = compatibilidad(recurso, trabajo)

            if flag_recurso[recurso["id"]] == True:
                if recursos_libre[recurso["id"]] < menor:
                    menor = recursos_libre[recurso["id"]]
                else:
                    flag_recurso[recurso["id"]] = False

        for recurso in reversed(recursos):
            if flag_recurso[recurso["id"]] == True:
                duracion = trabajo["span"] / recurso["efficiency"]
                comienzo = recursos_libre[recurso["id"]]
                fin = comienzo + duracion
                retraso = max(0.0, fin - trabajo["deadline"])
                cumple = fin <= trabajo["deadline"]
                recursos_libre[recurso["id"]] = fin

                cronograma.append({"id": trabajo["id"], "recurso": recurso["id"], "inicio": comienzo, "fin": fin, "retraso": retraso, "cumple": cumple})
                cantidad_por_recurso[recurso["id"]] += duracion
                break
            flag_recurso[recurso["id"]] = False

    fin_ejecucion = time.time()
    ejecucion_total = fin_ejecucion - ejecucion

    return {"lista": cronograma, "tiempo_ms": ejecucion_total, "uso_recursos": cantidad_por_recurso}