from typing import List, Dict, Any 
import json
#datos de json 
with open ("data/resources-e01a.json","r") as recursosA: 
    recursos= json.load(recursosA)
    

with open ("data/works-e01b.json","r") as trabajoB: 
    trabajo= json.load(trabajoB)

def compatibilidad(recursos:Dict,trabajo:Dict)->bool: 
    return trabajo["category"]in recursos["categories"]



print(trabajo[0]["span"])