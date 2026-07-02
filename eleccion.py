import json
from pathlib import Path

ARCHIVO_POKEDEX = Path("pokedex.json")

class Pokemon:
    def __init__(self, nombre:str, numero:str, descripcion:str, tipos:list[str], hp:int, velocidad:int)->None:
        self.nombre = nombre
        self.numero = numero
        self.descripcion = descripcion
        self.tipos = tipos
        self.hp = hp
        self.velocidad = velocidad

    def mostrar_info(self):
        print(f"Pokédex: {self.nombre.upper()}")
        print(f"Número: #{self.numero}")
        print(f"Descripción: {self.descripcion}")
        print(f"Tipos: {', '.join(self.tipos)}")
        print(f"Vida (HP): {self.hp}")
        print(f"Velocidad: {self.velocidad}")
    
    def listar_nombres() -> None:
        try:
            with open(ARCHIVO_POKEDEX, "r", encoding="utf-8") as archivo:
                pokedex = json.load(archivo)
                
            print("Lista de Pokémon registrados:")
            for i, nombre in enumerate(pokedex.keys(), 1):
                print(f"{i}: {nombre}")
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {ARCHIVO_POKEDEX}")


    def seleccionar() -> 'Pokemon' | None:
        try:
            with open(ARCHIVO_POKEDEX, "r", encoding="utf-8") as archivo:
                pokedex = json.load(archivo)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {ARCHIVO_POKEDEX}")
            return None
            
        buscar = input("\nEscribe el nombre del Pokémon que buscas: ").strip().capitalize()
        
        if buscar in pokedex:
            datos = pokedex[buscar]
            
            pokemon_encontrado = Pokemon(
                nombre=buscar,
                numero=datos['numero'],
                descripcion=datos['descripcion'],
                tipos=datos['tipos'],
                hp=datos['estadisticas']['hp'],
                velocidad=datos['estadisticas']['velocidad']
            )
            
            pokemon_encontrado.mostrar_info()
            
            respuesta = input(f"¿Deseas seleccionar a {buscar}? (si/no): ").strip().lower()
            
            if respuesta == 'si':
                print(f"Has seleccionado a {buscar}")
                return pokemon_encontrado 
            else:
                print("Selección cancelada.")
                return None
                
        else:
            print(f"\nEl Pokémon '{buscar}' no se encontró en la base de datos.")
            return None

Pokemon.listar_nombres()
mi_pokemon = Pokemon.seleccionar()
