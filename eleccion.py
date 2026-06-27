import json
from pathlib import Path

ARCHIVO_POKEDEX = Path("pokedex.json")

def listar_nombres_pokemon() -> None:
    i=1    
    with open(ARCHIVO_POKEDEX, "r", encoding="utf-8") as archivo:
        pokedex = json.load(archivo)
        
    print("Lista de Pokémon registrados:")
    
    for nombre in pokedex.keys():
        print(f"{i}: {nombre}")
        i=i+1
        
def seleccionar_pokemon():
    with open(ARCHIVO_POKEDEX, "r", encoding="utf-8") as archivo:
        pokedex = json.load(archivo)
     
    buscar = input("Escribe el nombre del Pokémon que buscas: ").strip().capitalize()
    
    if buscar in pokedex:
        datos = pokedex[buscar]
        print(f" Pokédex: {buscar.upper()}")
        print(f"Número: #{datos['numero']}")
        print(f"Pokedex: {datos['descripcion']}")
        print(f"Tipos: {', '.join(datos['tipos'])}")
        print(f"Vida (HP): {datos['estadisticas']['hp']}")
        print(f"Velocidad: {datos['estadisticas']['velocidad']}")
        
        respuesta = input(f"¿Deseas seleccionar a {buscar}?: si/no ").strip().lower()
        
        if respuesta == 'si':
            print(f"Has seleccionado a {buscar}!")
            return
        #Aqui se supone que guarda el pokemon pero aun no se como funcionaria 
        else:
            print("Selección cancelada.")
            return
            
    else:
        print(f"\nEl Pokémon '{buscar}' no se encontró en la base de datos.")
        return

listar_nombres_pokemon()
seleccionar_pokemon()
