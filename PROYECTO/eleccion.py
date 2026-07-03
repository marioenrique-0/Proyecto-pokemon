import json
import streamlit as st
from pathlib import Path

ARCHIVO_POKEDEX = Path("pokedex.json")

class Pokemon:
    def __init__(self, nombre:str, numero:int, descripcion:str, tipos:list[str], hp:int, ataque:int, defensa:int, velocidad:int, sprite:str, ataques:dict)->None:
        self.nombre = nombre
        self.numero = numero
        self.descripcion = descripcion
        self.tipos = tipos
        self.hp = hp
        self.ataque = ataque
        self.defensa = defensa
        self.velocidad = velocidad
        self.sprite = sprite
        self.ataques = ataques
        
    def mostrar_info(self):
        st.header(f"{self.nombre.upper()} - #{self.numero}")
        try:
            st.image(self.sprite, width=200)
        except:
            st.warning("Imagen no encontrada.")
        
        # Mostramos todas las estadísticas
        st.write(f"**Tipos:** {', '.join(self.tipos)}")
        col1, col2 = st.columns(2)
        col1.write(f"**HP:** {self.hp}")
        col1.write(f"**Ataque:** {self.ataque}")
        col2.write(f"**Defensa:** {self.defensa}")
        col2.write(f"**Velocidad:** {self.velocidad}")
        
        st.write("**Ataques:**")
        for nombre_ataque, info in self.ataques.items():
            st.write(f"- **{nombre_ataque}**: {info['tipo']} | Potencia: {info['potencia']} | Precisión: {info['precision']}")

    @classmethod
    def seleccionar(cls, pokedex: dict) -> 'Pokemon' | None:
        nombres_pokemon = list(pokedex.keys())
        buscar = st.selectbox("Elige un Pokémon:", nombres_pokemon, key="selector_pkmn")
        
        if buscar:
            datos = pokedex[buscar]
            stats = datos['estadisticas'] # Accedemos al diccionario de estadísticas
            
            pkmn = cls(
                nombre=buscar,
                numero=datos['numero'],
                descripcion=datos['descripcion'],
                tipos=datos['tipos'],
                hp=stats['hp'],
                ataque=stats['ataque'],
                defensa=stats['defensa'],
                velocidad=stats['velocidad'],
                sprite=datos.get('sprite', 'Sprites/default.png'),
                ataques=datos['ataques']
            )
            pkmn.mostrar_info()
            if st.button(f"Añadir {buscar} al equipo"):
                return pkmn
        return None

# ==========================================
# CÓDIGO PRINCIPAL
# ==========================================
st.title("Selección de Equipos Pokémon")

# Inicialización de memoria
if "jugador_actual" not in st.session_state: st.session_state.jugador_actual = 1
if "equipo_j1" not in st.session_state: st.session_state.equipo_j1 = []
if "equipo_j2" not in st.session_state: st.session_state.equipo_j2 = []
if "confirmando" not in st.session_state: st.session_state.confirmando = False

try:
    with open(ARCHIVO_POKEDEX, "r", encoding="utf-8") as f: pokedex = json.load(f)
except:
    st.error("Archivo no encontrado")
    st.stop()

equipo_activo = st.session_state.equipo_j1 if st.session_state.jugador_actual == 1 else st.session_state.equipo_j2

st.subheader(f"Turno del Jugador {st.session_state.jugador_actual}")
st.write(f"Pokémon seleccionados: {len(equipo_activo)}/6")

if len(equipo_activo) < 6:
    resultado = Pokemon.seleccionar(pokedex)
    if resultado:
        equipo_activo.append(resultado)
        st.rerun()
elif not st.session_state.confirmando:
    st.success("¡Equipo de 6 completado!")
    for p in equipo_activo: st.write(f"- {p.nombre}")
    
    if st.button("SIGUIENTE"):
        st.session_state.confirmando = True
        st.rerun()
else:
    st.warning("¿Confirmas tu equipo definitivo?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("SÍ, CONFIRMO"):
            if st.session_state.jugador_actual == 1:
                st.session_state.jugador_actual = 2
                st.session_state.confirmando = False
                st.rerun()
            else:
                st.balloons()
                st.write("Ambos equipos listos. ¡Que comience el combate!")
    with col2:
        if st.button("NO, REINICIAR EQUIPO"):
            equipo_activo.clear()
            st.session_state.confirmando = False
            st.rerun()
