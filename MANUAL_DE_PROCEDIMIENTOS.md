# 🕹️ MANUAL DE PROCEDIMIENTOS: VIRTUAL LUDOTECA RPG

Bienvenido al manual operativo de tu Ludoteca Virtual de 16-bits. Este documento detalla cómo funciona el sistema, cómo encenderlo y cómo mantenerlo actualizado.

---

## 1. DESCRIPCIÓN DEL SISTEMA
El sistema es una aplicación web interactiva que simula un videoclub de los años 90 en vista "Top-Down 2D" (vista desde arriba estilo Zelda/Pokémon). En este entorno virtual, controlas a un avatar para navegar por pasillos físicos y explorar tu colección real de juegos de mesa.

La aplicación consta de dos partes principales:
1. **Frontend (`index.html`)**: El motor gráfico que dibuja el mapa, maneja los controles del personaje y muestra las ventanas de los juegos.
2. **Backend (`server.py`)**: Un pequeño servidor local inteligente en Python que permite alojar la página y recibir las imágenes nuevas que subes.

---

## 2. CÓMO ENCENDER EL SISTEMA

Como la aplicación guarda imágenes directamente en tu computadora de forma segura, requiere que su propio "servidor" esté encendido.

**Pasos para arrancar:**
1. Abre tu terminal de comandos (PowerShell o CMD).
2. Navega hasta la carpeta de tu proyecto:
   `cd "c:\Users\astud\OneDrive\Juegos de mesa"`
3. Ejecuta el servidor de Python:
   `python server.py`
4. El servidor quedará escuchando en segundo plano en el puerto `7560`.

**Para acceder:**
Abre tu navegador de preferencia (Chrome, Edge, Firefox) e ingresa a la siguiente dirección:
👉 **[http://127.0.0.1:7560](http://127.0.0.1:7560)**

---

## 3. CONTROLES Y NAVEGACIÓN

El sistema detecta automáticamente tu teclado:
- **Movimiento**: Utiliza las **Flechas Direccionales** (`Arriba, Abajo, Izquierda, Derecha`) o las teclas **W, A, S, D** para caminar por los pasillos.
- **Identificar Juegos**: Cuando camines y te pongas de frente a un estante (resaltado en neón rosa), aparecerá un cartel flotante que te dirá el nombre del juego que estás mirando.
- **Interactuar / Abrir**: Estando frente a un juego, presiona la tecla **`ENTER`**. Esto abrirá la ventana emergente con la portada gigante, las estadísticas y la valoración de BoardGameGeek.
- **Cerrar**: Presiona `ESCAPE` o la `X` roja en la esquina para cerrar el juego y volver a caminar.

---

## 4. GESTIÓN DE PORTADAS Y MANTENIMIENTO

Debido a que BoardGameGeek posee un cortafuegos (Cloudflare) muy estricto que bloquea a los robots automáticos, la descarga de portadas se realiza de forma semi-manual, la cual es 100% segura y libre de bloqueos.

### ¿Cómo actualizar o agregar la portada de un juego?
1. Camina con tu avatar hasta el juego que deseas modificar y presiona `ENTER`.
2. Verás que en los detalles aparece el botón amarillo **`[ UPLOAD COVER ]`**.
3. Haz clic en él y selecciona una imagen desde tu computadora (puedes descargar previamente la imagen oficial desde Google Imágenes o desde el botón azul `[ VER EN BGG ]`).
4. ¡Listo! El servidor `server.py` procesará el archivo y lo guardará de forma permanente en la carpeta `portadas/`. La estantería se actualizará al instante sin necesidad de recargar la página.

### ¿Cómo añadir juegos nuevos en el futuro?
La lista actual de más de 40 juegos está guardada dentro del archivo `games_with_images.json`.
1. Abre `games_with_images.json` con cualquier editor de texto.
2. Copia el bloque de un juego existente y pégalo al final de la lista, modificando los campos (`name`, `players`, `difficulty`, `type`, `rating`, `image`).
3. IMPORTANTE: Para que el motor 2D lo reconozca, **debes actualizar el bloque `<script>` de `index.html`** inyectándole este nuevo JSON o pedirle al sistema (IA) que lo recompile.

---

## 5. SOLUCIÓN DE PROBLEMAS

- **Error de conexión al subir la portada**: Verifica que la consola de PowerShell donde corriste `python server.py` sigue abierta y no se ha cerrado.
- **La página no carga**: Asegúrate de estar ingresando a `127.0.0.1:7560` y no abriendo directamente el archivo `.html` haciendo doble clic, ya que los navegadores bloquean la subida de archivos locales por motivos de seguridad si no hay un servidor de por medio.
