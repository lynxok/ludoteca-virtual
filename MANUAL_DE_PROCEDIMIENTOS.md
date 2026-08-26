# 🕹️ MANUAL DE PROCEDIMIENTOS: REINO LUDOTECA QUEST (v2.0)

Bienvenido al manual operativo y de arquitectura de tu **Ludoteca Virtual Medieval en 2D (Tiny Swords / Agent Quest Engine)**.

---

## 1. DESCRIPCIÓN GENERAL
La aplicación es una experiencia interactiva web donde tu colección real de más de 40 juegos de mesa ha sido transformada en un **Reino Abierto Medieval navegable**.

### Elementos Principales:
1. **Archipiélago de 4 Distritos Temáticos**:
   - 🏡 **Distrito Familiar**: Juegos de estrategia accesible (*Catan, Carcassonne, Aventureros al Tren, Azul...*).
   - 🎉 **Distrito Party**: Risas, cartas rápidas y humor (*Munchkin, Taco Gato, Con Eso No Se Jode, CACA...*).
   - 👑 **Distrito Real**: Estrategia pesada y expertos (*Root, Wingspan, The White Castle, The Red Cathedral...*).
   - 🃏 **Distrito Secreto**: Deducción y roles ocultos (*Secret Hitler, Saboteur, Hombres Lobo, Just One...*).
2. **Casas y Miniaturas en los Techos**:
   - Cada juego tiene su propia casa/edificio.
   - En el tejado de cada casa se exhibe la **miniatura oficial de la portada** en un marco de madera noble, permitiendo reconocer cualquier juego a simple vista sin necesidad de leer carteles.
3. **Fichas con Sinopsis Rápida**:
   - Cada juego incluye una explicación de 2 líneas sobre de qué trata y cómo se juega, además de su valoración de BGG y enlace a tutoriales.
4. **Sistema de Movimiento por Clic / Toque (Pathfinding A*)**:
   - Puedes caminar haciendo clic o tocando el terreno (estilo *Age of Empires*), usando la cruceta D-Pad o con las teclas `WASD / Flechas`.

---

## 2. NAVEGACIÓN Y CONTROLES

| Acción | En Computadora (PC) | En Teléfono / Tablet |
| :--- | :--- | :--- |
| **Moverse por el reino** | Clic en el suelo / `WASD` / `Flechas` | Tocar el suelo / Usar D-Pad virtual |
| **Entrar a una casa** | Clic en la casa / `ENTER` frente a la puerta | Tocar la casa / Botón circular `⚔️ ENTRAR` |
| **Buscador Rápido** | Escribir en la barra `🔍 Buscar juego...` | Escribir en la barra `🔍 Buscar juego...` |
| **Viaje Rápido entre Islas** | Clic en `[🏡 Familiares | 🎉 Party | 👑 Expertos | 🃏 Deducción]` | Tocar los botones de islas |
| **Minimapa** | Clic en el minimapa (esquina superior derecha) | Tocar el minimapa |
| **Cambiar de Héroe** | Clic en `👤 HÉROE` | Tocar `👤 HÉROE` |
| **Guía del Reino** | Clic en `📜 GUÍA` | Tocar `📜 GUÍA` |

---

## 3. GESTIÓN Y SUBIDA DE PORTADAS

El sistema cuenta con un motor de subida universal dual (funciona tanto en local como en producción):

### ¿Cómo subir o cambiar la portada de un juego?
1. Abre la ficha de cualquier juego (tocando su casa o buscándolo arriba).
2. Haz clic en el botón verde **`[ SUBIR PORTADA ]`**.
3. Selecciona la imagen desde tu dispositivo.
4. **En Hostinger (`juegosdemesa.lnx.com.ar`)**: El archivo `upload.php` procesará la imagen y la guardará de inmediato en la carpeta `portadas/`.
5. **En Local (`127.0.0.1:7560`)**: `server.py` recibirá el archivo y lo guardará en `portadas/`.
6. ¡La miniatura en el techo de la casa y la portada de la ficha se actualizarán automáticamente sin recargar la página!

---

## 4. DESPLIEGUE Y SINCRONIZACIÓN CON HOSTINGER

El repositorio oficial está alojado en:
👉 **`https://github.com/lynxok/ludoteca-virtual`**

Cada vez que se suben mejoras o portadas nuevas:
1. Entra a **Hostinger hPanel** ➔ **Avanzado** ➔ **GIT**.
2. Haz clic en el botón **Desplegar (Deploy)** / **Actualizar**.
3. El sitio web público (`https://juegosdemesa.lnx.com.ar`) se actualizará en segundos.
