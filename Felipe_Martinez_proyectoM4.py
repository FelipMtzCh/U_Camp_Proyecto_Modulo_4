import requests
import matplotlib.pyplot as plt
from PIL import Image
from urllib.request import urlopen
from pathlib import Path
import json

def Ingresa_Pokemon():
    """
    Solicita al usuario el nombre de un Pokémon.

    Valida que el nombre contenga únicamente letras y repite
    la solicitud hasta que se ingrese un valor válido. Una vez
    validado, consulta la información del Pokémon ingresado.
    """

    # Almacena el nombre ingresado por el usuario
    pokemon = ""
    
    # Solicita el nombre hasta que sea válido
    while pokemon == "":
        pokemon = input("Ingresa el nombre de un Pokémon: ").lower().strip()
        
        # Verificar que solo tenga letras
        if not pokemon.isalpha():
            pokemon = ""
            print("\nError: solo puedes ingresar nombres de Pokémon (sin números ni caracteres especiales). Intenta de nuevo.")
            
    # Consulta la información del Pokémon ingresado
    Obtener_Pokemon(pokemon)


def Obtener_Pokemon(pokemon):
    """
    Busca un Pokémon en la PokeAPI utilizando el nombre ingresado.

    Si el Pokémon existe, obtiene sus datos y los envía para
    ser procesados. Si no existe, permite al usuario intentar
    nuevamente o cerrar el programa.
    """

    # Construye la URL de consula para el Pokémon
    url = "https://pokeapi.co/api/v2/pokemon/" + pokemon
    
    # Realiza la petición a la API
    try:
        respuesta = requests.get(url, timeout=10)
    except requests.Timeout:
        print("Error: la solicitud tardó demasiado en responder (timeout).\nIntenta nuevamente más tarde.")
        return
        
    # Si el Pokémon existe, obtiene y procesa sus datos
    if respuesta.status_code == 200:
        datos = respuesta.json()
        Obtener_Datos(datos)

    # Si no existe, el usuario puede elegir intentar o cerrar el programa
    elif respuesta.status_code != 200:
        print("\nNo se encontró ningún Pokémon con ese nombre.\n")
        
        print("""
    ========================================
    ¿Qué deseas hacer?
    ========================================
    (SI) Intentar con otro Pokémon
    (NO) Salir del programa
    ========================================
        """)
        
        while True:
            opcion = input("Selecciona una opción (SI/NO): ").upper().strip()
            if opcion == "SI":
                Ingresa_Pokemon()
                break
            elif opcion == "NO":
                print("Gracias por usar la Pokédex. ¡Hasta luego!")
                break
            else:
                print("Opción inválida. Por favor escribe SI o NO.\n")

def Obtener_Datos(datos_json):
    """
    Extrae y organiza la información de un Pokémon obtenida
    desde la PokeAPI.

    Obtiene datos como nombre, imagen, altura, peso, tipos,
    habilidades, movimientos y estadísticas. Finalmente,
    guarda la información en un archivo JSON y la muestra
    mediante gráficas.
    """

    # Obtiene la imagen del Pokémon
    imagen = None
    try:
        url_imagen = datos_json["sprites"]["front_default"]

        if url_imagen:
            imagen = Image.open(urlopen(url_imagen))
    except:
        print("El pokémon no tiene imagen")
        
    # Extrae los datos generales del Pokémon
    nombre = datos_json["name"]
    altura = datos_json["height"] / 10
    peso = datos_json["weight"] / 10
    tipos = [t["type"]["name"] for t in datos_json["types"]]
    habilidades = [h["ability"]["name"] for h in datos_json["abilities"]]

    # Obtiene los últimos 4 movimientos o todos si tiene menos
    total_mov = len(datos_json["moves"])
    movimientos = []

    if total_mov > 4:
        mov = 1
        while mov < 5:
            movimientos.append(datos_json["moves"][total_mov - mov]["move"]["name"])
            mov += 1
    else:
        movimientos = [m["move"]["name"] for m in datos_json["moves"]]

    # Organiza las estadísticas principales
    estadisticas = {
        "Vida": datos_json["stats"][0]["base_stat"],
        "Ataque": datos_json["stats"][1]["base_stat"],
        "Defensa": datos_json["stats"][2]["base_stat"],
        "Ataque Especial": datos_json["stats"][3]["base_stat"],
        "Defensa Especial": datos_json["stats"][4]["base_stat"],
        "Velocidad": datos_json["stats"][5]["base_stat"]
    }

    # Agrupa toda la información en un diccionario
    pokemon = {
        "nombre" : nombre, 
        "url_imagen" : url_imagen, 
        "altura" : f"{altura} m", 
        "peso" : f"{peso} kg", 
        "tipos" : tipos, 
        "habilidades" : habilidades, 
        "movimientos" : movimientos, 
        "estadisticas" : estadisticas
    }

    # Guarda y muestra la información del Pokémon
    Crea_Archivo_Json(pokemon)
    GraficarPokemon(pokemon)

def GraficarPokemon(pokemon):
    """
    Muestra la información de un Pokémon en una ventana gráfica.

    Presenta la imagen y datos generales del Pokémon en un panel,
    junto con una gráfica de barras que muestra sus estadísticas.
    """

    imagen = None

    # Carga la imagen del Pokémon desde la URL almacenada
    try:
        if pokemon["url_imagen"]:
            imagen = Image.open(urlopen(pokemon["url_imagen"]))
    except:
        print("No se pudo cargar la imagen")

    # Construye el texto descriptivo del Pokémon
    descripcion = f"""
    {pokemon['nombre'].upper()}
    Peso: {pokemon['peso']}
    Altura: {pokemon['altura']}
    Movimientos: {", ".join(pokemon['movimientos'])}
    Habilidades: {", ".join(pokemon['habilidades'])}
    Tipo: {", ".join(pokemon['tipos'])}
    """

    # Crea dos paneles: información e estadísticas
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Muestra la imagen del Pokémon
    if imagen:
        ax1.imshow(imagen)

    # Agrega la descripción debajo de la imagen
    ax1.axis("off")
    ax1.text(
        0.5,
        -0.15,
        descripcion,
        transform=ax1.transAxes,
        ha="center"
    )

    # Obtiene las estadísticas del Pokémon
    estadisticas = pokemon["estadisticas"]

    # Genera una gráfica de barras horizontales
    ax2.barh(estadisticas.keys(), estadisticas.values())
    ax2.set_title("Estadísticas")

    # Muestra la ventana con las gráficas
    plt.show()

def Crea_Archivo_Json (pokemon_datos):
    """
    Guarda la información de un Pokémon en un archivo JSON.

    Si la carpeta Pokedex no existe, la crea automáticamente.
    El archivo se guarda utilizando el nombre del Pokémon.
    """

    # Obtiene la ruta donde se encuentra el programa
    ruta_programa = Path(__file__).parent

    # Crea la carpeta Pokedex si aún no existe
    carpeta_pokedex = ruta_programa / "Pokedex"
    carpeta_pokedex.mkdir(exist_ok=True)

    # Define la ruta y nombre del archivo JSON
    arhivo_pokemon = carpeta_pokedex / (f"{pokemon_datos['nombre']}.json")

    # Guarda los datos del Pokémon en formato JSON
    with open(arhivo_pokemon, "w", encoding="utf-8") as f_pokemon:
        json.dump(pokemon_datos, f_pokemon, indent=4, ensure_ascii=False)


print(""" 
========================================================
        Bienvenido a mi proyecto POKEDEX
========================================================
    Explora el mundo Pokémon desde tu consola.

Ingresa el nombre de cualquier Pokémon para consultar:

• Imagen del Pokémon
• Tipo o tipos
• Peso y altura
• Habilidades
• Movimientos
• Estadísticas principales

¡Comienza tu búsqueda y descubre información de tus
Pokémon favoritos!

========================================================
    """)
# Inicia la búsqueda de Pokémon
Ingresa_Pokemon()
