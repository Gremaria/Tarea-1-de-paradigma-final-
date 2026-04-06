from typing import List, Dict, Any 
import json
#datos de json 
with open ("data/resources-e01a.json","r") as recursosA: 
    recursos= json.load(recursosA)
    

with open ("data/works-e01b.json","r") as trabajoB: 
    trabajos= json.load(trabajoB)


# Funcion para evaluar si existe una categoria del trabajo en un recurso dado
def compatibilidad(recursos:Dict,trabajo:Dict)->bool: 
    return trabajo["category"]in recursos["categories"]


def tiempos_cronograma(recursos: Dict, trabajos: Dict) -> dict:

    # se ordena el diccionario de trabajos de mayor a menor
    trabajos = sorted(trabajos, key=lambda x: x["span"], reverse=True)

    contadores = {}    # variable que lleva cuenta de cuanto tiempo lleva ocupado un recurso
    flag_recurso = {}  # variable que representa si un recurso es compatible con el trabajo siendo loopeado

    for recurso in recursos:
        contadores[recurso["id"]] = 0
        flag_recurso[recurso["id"]] = False

    for trabajo in trabajos:
        menor = 10000 #valor arbitrario grande

        for recurso in recursos:
            flag_recurso[recurso["id"]] = compatibilidad(recurso, trabajo)

            if (flag_recurso[recurso["id"]] == True) and (contadores[recurso["id"]] <= menor):
                menor = contadores[recurso["id"]] - 1
                #si los valores son compatibles y el tiempo que el recurso lleva ocupado es menor al menor valor registrado,
                #se reemplaza el menor valor con el del recurso menos 1, ya que empates son irrelevantes
            else:
                flag_recurso[recurso["id"]] = False
                #se reinicia a falso, necesario si hay compatibilidad pero el tiempo es mayor al menor establecido

        for recurso in reversed(recursos): #se usa la lista al revés, ya que el último valor marcado como True es el relevante
            if flag_recurso[recurso["id"]] == True:
                contadores[recurso["id"]] += trabajo["span"]
                break
            flag_recurso[recurso["id"]] = False #se reinician todas las posibles compatibilidades a False

    return contadores #Se retorna una lista con el tiempo que lleva ocupado cada recurso en total