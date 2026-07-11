import json
import streamlit as st
from pathlib import Path
import random

ARCHIVO_POKEDEX = Path("pokedex.json")
TABLA_TIPOS= Path("tabla.json")

# 1. Inicialización de la pantalla principal
if "pantalla_actual" not in st.session_state:
    st.session_state.pantalla_actual = "menu"
def cargar_tabla_tipos() -> dict:
    with open(TABLA_TIPOS, "r", encoding="utf-8") as f:
        tabla_tipos = json.load(f)
        return tabla_tipos

class Pokemon:
    def __init__(self, nombre: str, numero: int, descripcion: str, tipos: list[str], hp: int, ataque: int, defensa: int, velocidad: int, sprite: str, ataques: dict) -> None:
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
    # NOTA: equipo_excluido ahora es un diccionario (dict)
    def seleccionar(cls, pokedex: dict, equipo_excluido: dict) -> 'Pokemon | None':
        todos_los_nombres = list(pokedex.keys())
        
        # Extraemos los nombres de los objetos guardados en los VALUES del diccionario
        nombres_elegidos = [p.nombre for p in equipo_excluido.values()]
        
        buscar = st.selectbox("Elige un Pokémon:", todos_los_nombres, key="selector_pkmn")
        
        if buscar:
            datos = pokedex[buscar]
            stats = datos['estadisticas']
            
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
            
            if buscar in nombres_elegidos:
                st.error(f"¡Ya tienes a {buscar} en tu equipo! Por favor, elige uno diferente.")
            else:
                if st.button(f"Añadir {buscar} al equipo"):
                    return pkmn
        return None
# 3. Función de Selección de Equipos (Turnos Alternos)
def selecion():
    st.title("Selección de Equipos Pokémon")

    if "jugador_actual" not in st.session_state: st.session_state.jugador_actual = 1
    # INICIALIZAR COMO DICCIONARIOS {} en lugar de listas []
    if "equipo_j1" not in st.session_state: st.session_state.equipo_j1 = {}
    if "equipo_j2" not in st.session_state: st.session_state.equipo_j2 = {}

    try:
        with open(ARCHIVO_POKEDEX, "r", encoding="utf-8") as f: 
            pokedex = json.load(f)
    except:
        st.error("Archivo no encontrado")
        st.stop()

    # --- MOSTRAR EQUIPOS EN DOS COLUMNAS ---
    st.write("### Equipos Actuales")
    col_j1, col_j2 = st.columns(2)
    
    with col_j1:
        st.markdown(f"**Jugador 1 ({len(st.session_state.equipo_j1)}/6)**")
        # Como las keys ya son el texto formateado, solo las imprimimos
        for clave_formateada in st.session_state.equipo_j1.keys():
            st.write(clave_formateada)
            
    with col_j2:
        st.markdown(f"**Jugador 2 ({len(st.session_state.equipo_j2)}/6)**")
        # Imprimimos las keys directamente
        for clave_formateada in st.session_state.equipo_j2.keys():
            st.write(clave_formateada)

    st.divider()

    # --- LÓGICA DE TURNOS O FIN DE SELECCIÓN ---
    if len(st.session_state.equipo_j1) == 6 and len(st.session_state.equipo_j2) == 6:
        st.success("¡Ambos equipos están completos!")
                
        col1, col2 = st.columns(2)
        with col1:
            if st.button("¡COMENZAR COMBATE!"):
                st.session_state.pantalla_actual = "combate" 
                st.rerun()
        with col2:
            if st.button("REINICIAR EQUIPOS"):
                # .clear() funciona igual para vaciar diccionarios
                st.session_state.equipo_j1.clear()
                st.session_state.equipo_j2.clear()
                st.session_state.jugador_actual = 1
                st.rerun()
    else:
        st.subheader(f"Turno del Jugador {st.session_state.jugador_actual}")
        
        equipo_activo = st.session_state.equipo_j1 if st.session_state.jugador_actual == 1 else st.session_state.equipo_j2
        
        if len(equipo_activo) < 6:
            resultado = Pokemon.seleccionar(pokedex, equipo_activo)
            if resultado:
                # CREAMOS LA KEY CON EL FORMATO SOLICITADO
                numero_pokemon = len(equipo_activo) + 1
                clave_diccionario = f"{numero_pokemon}. {resultado.nombre}"
                
                # GUARDAMOS EN EL DICCIONARIO
                equipo_activo[clave_diccionario] = resultado
                
                # Cambiar de turno
                st.session_state.jugador_actual = 2 if st.session_state.jugador_actual == 1 else 1
                st.rerun()
        else:
            st.session_state.jugador_actual = 2 if st.session_state.jugador_actual == 1 else 1
            st.rerun()
        
    

def combate():
    if "pokemon_activo_j1" not in st.session_state:
        st.session_state.pokemon_activo_j1 = None
    if "pokemon_activo_j2" not in st.session_state:
        st.session_state.pokemon_activo_j2 = None

    # Variables para guardar lo que eligió cada uno
    if "accion_j1" not in st.session_state:
        st.session_state.accion_j1 = None
    if "accion_j2" not in st.session_state:
        st.session_state.accion_j2 = None

    j1 = pokemones_jugador(1)
    j2 = pokemones_jugador(2)

    # Fase 1: Elegir los Pokémon iniciales
    if st.session_state.pokemon_activo_j1 is None:
        elegir_primero(1, j1)
        
    elif st.session_state.pokemon_activo_j2 is None:
        st.info(f"El Jugador 1 enviará a **{st.session_state.pokemon_activo_j1.nombre}** a la batalla.")
        elegir_primero(2, j2)
        
    # Fase 2: Comienza la arena de combate
    else:
        menu_combate()

def guardar_accion(num_jugador: int, tipo_accion: str, valor):
    # Guardamos si eligió "ataque" o "cambio", y el nombre del ataque o el nuevo Pokémon
    accion = {"tipo": tipo_accion, "valor": valor}
    
    if num_jugador == 1:
        st.session_state.accion_j1 = accion
    else:
        st.session_state.accion_j2 = accion
        
    st.rerun()

def mostrar_menu_acciones(num_jugador: int, pokemon_activo: Pokemon, equipo: dict):
    # Variable para saber si estamos viendo los ataques o la mochila de Pokémon
    var_menu = f"viendo_menu_j{num_jugador}"
    if var_menu not in st.session_state:
        st.session_state[var_menu] = "ataques"
        
    # --- MENÚ DE ATAQUES ---
    if st.session_state[var_menu] == "ataques":
        st.write(f"**¿Qué hará {pokemon_activo.nombre}?**")
        
        # Mostrar botones de ataque
        for nombre_ataque, datos in pokemon_activo.ataques.items():
            if st.button(f"⚔️ {nombre_ataque}", key=f"btn_atk_j{num_jugador}_{nombre_ataque}"):
                guardar_accion(num_jugador, "ataque", nombre_ataque)
        
        st.write("---")
        # Mostrar botón para cambiar Pokémon
        if st.button("🔄 Cambiar Pokémon", key=f"btn_cambiar_j{num_jugador}"):
            st.session_state[var_menu] = "cambio"
            st.rerun()
            
    # --- MENÚ DE CAMBIO DE POKÉMON ---
    elif st.session_state[var_menu] == "cambio":
        st.write("**Elige un nuevo Pokémon:**")
        if st.button("⬅️ Volver a ataques", key=f"btn_volver_j{num_jugador}"):
            st.session_state[var_menu] = "ataques"
            st.rerun()
            
        # Mostrar equipo disponible
        for nombre_lista, pokemon_lista in equipo.items():
            # Evita mostrar el Pokémon que ya está peleando o los que tengan 0 HP
            if pokemon_lista.nombre != pokemon_activo.nombre and pokemon_lista.hp > 0:
                if st.button(f"Sacar a {pokemon_lista.nombre} (HP: {int(pokemon_lista.hp)})", key=f"btn_sel_cambio_j{num_jugador}_{pokemon_lista.nombre}"):
                    guardar_accion(num_jugador, "cambio", pokemon_lista)
                    st.session_state[var_menu] = "ataques" # Reiniciar menú para el próximo turno

def elegir_primero(num_jugador: int, equipo: dict)->Pokemon:
    st.write(f"### Jugador {num_jugador}: Elige tu Pokémon para empezar")
    
    # Creamos columnas para poner los botones uno al lado del otro
    columnas = st.columns(len(equipo))
    
    for i, (nombre, pokemon) in enumerate(equipo.items()):
        with columnas[i]:
            # 1. Mostramos el nombre en negrita
            st.markdown(f"**{pokemon.nombre}**")
            
            # 2. Mostramos la imagen (usando .sprite)
            st.image(pokemon.sprite, width=100)
            
            # 3. El botón para elegirlo queda debajo
            if st.button("Elegir", key=f"btn_elegir_j{num_jugador}_{nombre}"):
                
                # Dependiendo del jugador, guardamos su elección
                if num_jugador == 1:
                    st.session_state.pokemon_activo_j1 = pokemon
                else:
                    st.session_state.pokemon_activo_j2 = pokemon
                    
                # Recargamos la pantalla
                st.rerun()

def pokemones_jugador(jugador: int)-> dict:
    pokemones_j = {}
    equipo_base = st.session_state.equipo_j1 if jugador == 1 else st.session_state.equipo_j2
    for pokemon in equipo_base.values():
        pokemones_j[pokemon.nombre] = pokemon 
    return pokemones_j  

def atacar(atacante: Pokemon, objetivo: Pokemon, nombre_ataque: str):
    # Accedemos directamente a los datos del ataque usando su nombre
    datos_ataque = atacante.ataques[nombre_ataque]
    
    potencia = datos_ataque['potencia']
    precision = datos_ataque['precision']
    tipo = datos_ataque['tipo']
    
    # Imprimimos qué está pasando
    st.write(f"**{atacante.nombre}** intenta usar **{nombre_ataque}**...")
    
    # Calculamos si acierta o falla
    if random.randint(1, 100) > precision:
        st.warning(f"¡El ataque ha fallado!")
    else:
        # Calculamos y aplicamos el daño
        d = daño(atacante, objetivo, potencia, tipo)
        actualizar_hp(objetivo, d)
        st.success(f"¡Es un golpe directo! Causó {int(d)} puntos de daño.")
        
def daño(atacante:Pokemon, objetivo: Pokemon, potencia:int, tipo:str)-> float:
    E,B= 1,1
    if tipo in atacante.tipos:
        B*=1.5
    critico=random.randint(1,100)
    if critico<=6.25:
        B*=2
    tipos_objetivo = objetivo.tipos
    tabla=cargar_tabla_tipos()
    for tipo_objetivo in tipos_objetivo:
        E *= tabla[tipo][tipo_objetivo]
    d=0.01*B*E*(((0.2*10+1)*potencia*atacante.ataque/objetivo.defensa*25)+2)
    return d
def actualizar_hp(objetivo: Pokemon, daño: float):
    objetivo.hp -= daño
    if objetivo.hp < 0:
        objetivo.hp = 0
def menu_combate():
    st.subheader("⚔️ COMBATE ⚔️")
    st.divider()

    # --- FASE DE RESOLUCIÓN (Ambos han elegido) ---
    if st.session_state.accion_j1 is not None and st.session_state.accion_j2 is not None:
        
        accion1 = st.session_state.accion_j1
        accion2 = st.session_state.accion_j2

        # 1. RESOLVER CAMBIOS DE POKÉMON PRIMERO (Tienen prioridad de turno)
        if accion1["tipo"] == "cambio":
            st.session_state.pokemon_activo_j1 = accion1["valor"]
            st.info(f"🔄 ¡El Jugador 1 cambió a {st.session_state.pokemon_activo_j1.nombre}!")
            
        if accion2["tipo"] == "cambio":
            st.session_state.pokemon_activo_j2 = accion2["valor"]
            st.info(f"🔄 ¡El Jugador 2 cambió a {st.session_state.pokemon_activo_j2.nombre}!")

        # Refrescamos las variables después de los posibles cambios
        pokemon1 = st.session_state.pokemon_activo_j1
        pokemon2 = st.session_state.pokemon_activo_j2
        
        st.divider()

        # 2. RESOLVER ATAQUES SEGÚN LA VELOCIDAD
        # Si ambos eligieron atacar
        if accion1["tipo"] == "ataque" and accion2["tipo"] == "ataque":
            if pokemon1.velocidad >= pokemon2.velocidad:
                atacar(pokemon1, pokemon2, accion1["valor"])
                if pokemon2.hp > 0:
                    atacar(pokemon2, pokemon1, accion2["valor"])
            else:
                atacar(pokemon2, pokemon1, accion2["valor"])
                if pokemon1.hp > 0:
                    atacar(pokemon1, pokemon2, accion1["valor"])
                    
        # Si solo el J1 atacó (porque el J2 hizo un cambio)
        elif accion1["tipo"] == "ataque" and accion2["tipo"] == "cambio":
            atacar(pokemon1, pokemon2, accion1["valor"])
            
        # Si solo el J2 atacó (porque el J1 hizo un cambio)
        elif accion2["tipo"] == "ataque" and accion1["tipo"] == "cambio":
            atacar(pokemon2, pokemon1, accion2["valor"])

        st.divider()

        # Mostramos los Pokémon actualizados tras recibir los daños
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**{pokemon1.nombre}** - HP: {int(pokemon1.hp)}")
            st.image(pokemon1.sprite, width=150)
        with col2:
            st.write(f"**{pokemon2.nombre}** - HP: {int(pokemon2.hp)}")
            st.image(pokemon2.sprite, width=150)
            
        # Botón para reiniciar el turno y continuar
        if st.button("Siguiente turno"):
            st.session_state.accion_j1 = None
            st.session_state.accion_j2 = None
            st.rerun()
            
    # --- FASE DE ELECCIÓN EN COLUMNAS ---
    else:
        col1, col2 = st.columns(2)
        
        # COLUMNA DEL JUGADOR 1
        with col1:
            st.write(f"### Lado J1: {st.session_state.pokemon_activo_j1.nombre}")
            st.write(f"**HP: {int(st.session_state.pokemon_activo_j1.hp)}**")
            st.image(st.session_state.pokemon_activo_j1.sprite, width=150)
            
            # Si el Jugador 1 aún no elige, le mostramos sus opciones
            if st.session_state.accion_j1 is None:
                mostrar_menu_acciones(1, st.session_state.pokemon_activo_j1, pokemones_jugador(1))
            else:
                st.success("✅ Jugador 1 listo. Esperando al rival...")

        # COLUMNA DEL JUGADOR 2
        with col2:
            st.write(f"### Lado J2: {st.session_state.pokemon_activo_j2.nombre}")
            st.write(f"**HP: {int(st.session_state.pokemon_activo_j2.hp)}**")
            st.image(st.session_state.pokemon_activo_j2.sprite, width=150)
            
            # Si el Jugador 2 aún no elige, le mostramos sus opciones
            if st.session_state.accion_j2 is None:
                mostrar_menu_acciones(2, st.session_state.pokemon_activo_j2, pokemones_jugador(2))
            else:
                st.success("✅ Jugador 2 listo. Esperando al rival...")

def menus():    
    if st.session_state.pantalla_actual == "menu":
        st.subheader("MENU INICIAL")
        try:
            st.video("Intro.mp4")
        except:
            st.warning("Video no encontrado.")
                
        col1, col2 = st.columns(2)
        with col1:
            if st.button("JUGAR 1VS1"):
                st.session_state.modo_juego = "1vs1"       
                st.session_state.pantalla_actual = "juego" 
                st.rerun()
                    
        with col2:
            if st.button("JUGAR CONTRA BOT"):
                st.session_state.modo_juego = "bot"        
                st.session_state.pantalla_actual = "juego" 
                st.rerun()

    elif st.session_state.pantalla_actual == "juego":
        st.subheader(f"Modo de juego: {st.session_state.get('modo_juego', 'Normal')}")
        if st.button("Volver al Menú Principal"):
            st.session_state.pantalla_actual = "menu"
            st.rerun()
        selecion()
    elif st.session_state.pantalla_actual == "combate":
        combate()
menus()