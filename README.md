# U_Camp_Proyecto_Modulo_4

## Descripción

Este proyecto consiste en una **POKEDEX**, donde el usuario puede ingresar el nombre de un Pokémon para consultar su información utilizando la API de PokeAPI.
Al final, se grafica una imagen del pokémon ingresado junto con sus datos y estadisticas basica, ademas se crea una carpeta con nombre Pokedex dentro de la misma ubicación del programa, y dentro de la carpeta se crea un archivo con el nombre de cada pokémon consultado.

---

## Librerías utilizadas

- **Requests**
  Se utiliza para realizar peticiones a la API de PokeAPI y obtener los datos de los Pokémon.

- **Matplotlib**  
  Se utiliza para mostrar la imagen del Pokémon y generar una gráfica con las estadísticas.

- **PIL**
  Se utiliza para cargar la imagen del Pokémon obtenida desde la web.

- **Urlopen**
  Se utiliza para descargar la imagen del Pokémon desde una URL.

- **Path**
  Se utiliza para crear la carpeta Pokedex.

- **Json**
  Se utiliza para guardar la información de cada Pokémon en archivos .json.n

---

## Funcionamiento del programa

1. El programa muestra un mensaje de bienvenida al usuario.

2. Se solicita ingresar el nombre de un Pokémon.

3. Se valida que el nombre solo contenga letras.

4. Se realiza una consulta a la API de PokeAPI.

5. Si el Pokémon existe:
   - Se obtienen sus datos (nombre, tipo, peso, altura, habilidades, movimientos y estadísticas). 
   - Se descarga su imagen.
   - Se muestra una ventana con la imagen y una gráfica de estadísticas. 
   - Se guarda la información en un archivo JSON dentro de la carpeta Pokedex.

6. Si el Pokémon no existe:
   - Se muestra un mensaje de error.
   - El usuario puede intentar nuevamente o salir del programa.

---

## Resultado

El programa genera:
- Una carpeta llamada Pokedex 
- Archivos .json con la información de cada Pokémon consultado
- Una ventana gráfica con:
  - Imagen del Pokémon.
  - Estadísticas en forma de gráfica de barras

---

## Lo apredido

1. Manejo de solicitud GET en aplis.
2. Explorar los datos obtenidos de la PokeAPI.
3. Uso de la libreria Path para el manejo de carpetas y archivos.
4. Uso de la libreria Json para la creación de archivos Json, agregando identación para un mejor acomodo en el archivo.
  
