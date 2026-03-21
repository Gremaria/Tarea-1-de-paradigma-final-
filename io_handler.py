import json 
from rich.console import Console
from rich.table import Table
from typing import List, Dict, Any 
 
#datos de json 
with open ("data/resources-e01a.json","r") as xd: 
    recursos= json.load(xd)
    print(recursos)

print("--------------------------------------------------------------")

with open ("data/works-e01b.json","r") as w: 
    trabajo= json.load(w)
    print(trabajo)
    
for s in trabajo:
    print(s["span"])
print("-------------------------------------------------------------------------------------------------------------------------------------------")
# calculos de tiempo, como duracion, inicio, fin y dependencia 0
#Compatibilidad 
def compatibilidad(recursos:Dict,trabajo:Dict)->bool: 
    return trabajo["category"]in recursos["categories"]
print(compatibilidad(recursos[0], trabajo[0]))
#duracion: 
def calcular_duracion_real(trabajo: list, recursos: list) -> float:
   
    for t in trabajo: 
       
        for r in recursos:
            
            if t["category"] in r["categories"]:
              
                duracion = t["span"] / r["efficiency"]
                
                print(f"Tarea {t['id']} con {r['id']}: {duracion}")


                
  
    return duracion






