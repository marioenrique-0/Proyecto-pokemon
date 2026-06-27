import json
from pathlib import Path

ARCHIVO_POKEDEX = Path("pokedex.json")

def listar_nombres_pokemon() -> None:
    if not ARCHIVO_POKEDEX.exists():
        print("El archivo no existe.")
        return
        
    with open(ARCHIVO_POKEDEX, "r", encoding="utf-8") as archivo:
        pokedex = json.load(archivo)
        
    print("Lista de Pokémon registrados:")
    
    for nombre in pokedex.keys():
        print("-", nombre)

listar_nombres_pokemon()