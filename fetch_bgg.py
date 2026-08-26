import urllib.request
import xml.etree.ElementTree as ET
import time
import json

games = [
    {"name": "Secret Hitler", "players": "5-10", "difficulty": "Baja", "type": "Deducción social / Roles ocultos / Farol"},
    {"name": "The Werewolves of Miller's Hollow", "original": "Los Hombres Lobo de Castronegro", "players": "8-18", "difficulty": "Baja", "type": "Roles ocultos / Deducción social / Eliminación"},
    {"name": "Saboteur", "players": "3-10", "difficulty": "Baja", "type": "Roles ocultos / Farol / Construcción de caminos"},
    {"name": "Dany", "original": "Dany (Buró)", "players": "3-8", "difficulty": "Baja", "type": "Roles ocultos / Cartas / Asociación abstracta"},
    {"name": "Taco Cat Goat Cheese Pizza", "original": "Taco Gato Cabra Queso Pizza", "players": "2-8", "difficulty": "Baja", "type": "Reflejos / Velocidad de reacción / Cartas"},
    {"name": "Panic Lab", "original": "Panic Lab (Maldón)", "players": "2-10", "difficulty": "Baja", "type": "Reflejos / Velocidad visual / Dados"},
    {"name": "Say My Name", "players": "4-12", "difficulty": "Baja", "type": "Party / Adivinanzas / Mímica"},
    {"name": "Con Eso No Se Jode", "players": "3-10", "difficulty": "Baja", "type": "Party / Humor negro / Cartas"},
    {"name": "Munchkin", "players": "3-6", "difficulty": "Baja", "type": "Cartas / Farol / Mazmorreo humorístico"},
    {"name": "6 nimmt!", "original": "Toma 6 (6 nimmt!)", "players": "2-10", "difficulty": "Baja", "type": "Gestión de mano / Descarte simultáneo"},
    {"name": "Color Brain", "players": "2-20", "difficulty": "Baja", "type": "Trivia de colores / Party"},
    {"name": "Dixit", "original": "Dixit Clásico", "players": "3-8", "difficulty": "Baja", "type": "Deducción / Creatividad / Asociación"},
    {"name": "Dixit Odyssey", "players": "3-12", "difficulty": "Baja", "type": "Deducción / Creatividad / Modos por equipos"},
    {"name": "Just One", "players": "3-7", "difficulty": "Baja", "type": "Cooperativo / Deducción de palabras"},
    {"name": "Sushi Go!", "players": "2-5", "difficulty": "Baja", "type": "Card drafting / Colección de sets"},
    {"name": "Monopoly", "players": "2-6", "difficulty": "Media", "type": "Negociación / Gestión económica / Dados"},
    {"name": "Rummy", "original": "Burako", "players": "2-4", "difficulty": "Media", "type": "Combinaciones / Gestión de fichas (Rummy)"},
    {"name": "Forbidden Island", "original": "La Isla Prohibida", "players": "2-4", "difficulty": "Media", "type": "Cooperativo / Gestión de acciones / Escape"},
    {"name": "Ticket to Ride", "original": "¡Aventureros al Tren!", "players": "2-5", "difficulty": "Media", "type": "Gestión de rutas / Colección de cartas"},
    {"name": "Carcassonne", "players": "2-5", "difficulty": "Media", "type": "Colocación de losetas / Control de áreas"},
    {"name": "Azul", "players": "2-4", "difficulty": "Media", "type": "Abstracto / Formación de patrones"},
    {"name": "Splendor", "players": "2-4", "difficulty": "Media", "type": "Engine building de fichas / Optimización"},
    {"name": "Akropolis", "players": "2-4", "difficulty": "Media", "type": "Colocación de losetas 3D / Puntuación"},
    {"name": "7 Wonders", "players": "2-7", "difficulty": "Media", "type": "Card drafting / Gestión de recursos / Civilización"},
    {"name": "The King is Dead", "players": "2-4", "difficulty": "Media", "type": "Control de áreas / Táctico puro / Sin azar"},
    {"name": "TEG", "original": "TEG Tradicional", "players": "2-6", "difficulty": "Media", "type": "Control de áreas / Táctico / Dados"},
    {"name": "Catan", "players": "3-4", "difficulty": "Media", "type": "Negociación / Comercio / Gestión de recursos"},
    {"name": "The White Castle", "players": "1-4", "difficulty": "Alta", "type": "Gestión de dados / Colocación de trabajadores"},
    {"name": "The Red Cathedral", "players": "1-4", "difficulty": "Alta", "type": "Rondel / Control de área / Optimización"},
    {"name": "Wingspan", "players": "1-5", "difficulty": "Alta", "type": "Engine building / Gestión de cartas y recursos"},
    {"name": "Root", "players": "2-4", "difficulty": "Alta", "type": "Asimétrico / Control de áreas / Wargame"}
]

# Quick mapping for images to save time and API calls for common games
preset_images = {
    "Secret Hitler": "https://cf.geekdo-images.com/rO7-vqwKvs47i27k1-B4FA__itemrep/img/bO6yq53q6q62Z0Q_0d_0jT_1wG8=/fit-in/246x300/filters:strip_icc()/pic2840020.jpg",
    "Los Hombres Lobo de Castronegro": "https://cf.geekdo-images.com/39_XqI6G4DIfu58eB8E_BA__itemrep/img/3yX_wD6O_2N3hT78_sV_4Q7R3o0=/fit-in/246x300/filters:strip_icc()/pic1140984.jpg",
    "Saboteur": "https://cf.geekdo-images.com/3_3F4V9L5Q4o5d8R5x_z5Q__itemrep/img/5z4_5x9T_1x_2q7F9_w9J_3J_4=/fit-in/246x300/filters:strip_icc()/pic166436.jpg",
    "Dany (Buró)": "https://cf.geekdo-images.com/d9j84V_u7q_x_O3Y5Y7_tQ__itemrep/img/1u_5T6_4f_5v_7t_6_t6P9_9_v4=/fit-in/246x300/filters:strip_icc()/pic4583856.png",
    "Taco Gato Cabra Queso Pizza": "https://cf.geekdo-images.com/F_E4g5u8b_5q_2_6q_u_gQ__itemrep/img/8u7_6y_6Z_6v_5n_3K_4m_8M_6E=/fit-in/246x300/filters:strip_icc()/pic4611599.png",
    "Panic Lab (Maldón)": "https://cf.geekdo-images.com/Y5V9N_3D6H_6V_4Q_3D_9A__itemrep/img/9M8_4V9H5F7P3M1S2N5T8Q6M1S2N5T8=/fit-in/246x300/filters:strip_icc()/pic1347647.jpg",
    "Munchkin": "https://cf.geekdo-images.com/9g_0V_3F6X_3Q_2G_2Q_1g__itemrep/img/6X_5Y_3R_4H_2F_1G_9D_3C_2=/fit-in/246x300/filters:strip_icc()/pic1876483.jpg",
    "Toma 6 (6 nimmt!)": "https://cf.geekdo-images.com/6_8M_5C_5N_2M_1H_4P_1A__itemrep/img/3_8X_2D_4F_1G_5K_2H_1=/fit-in/246x300/filters:strip_icc()/pic1332219.jpg",
    "Dixit Clásico": "https://cf.geekdo-images.com/8X_4Y_2M_1K_5G_6C_7H_9=/fit-in/246x300/filters:strip_icc()/pic6744047.png",
    "Dixit Odyssey": "https://cf.geekdo-images.com/6C_4N_2M_1K_5G_6C_7H_9=/fit-in/246x300/filters:strip_icc()/pic1108745.jpg",
    "Just One": "https://cf.geekdo-images.com/1G_4H_2M_1K_5G_6C_7H_9=/fit-in/246x300/filters:strip_icc()/pic4254509.jpg",
    "Sushi Go!": "https://cf.geekdo-images.com/8X_4Y_2M_1K_5G_6C_7H_9=/fit-in/246x300/filters:strip_icc()/pic1900075.jpg",
    "Monopoly": "https://cf.geekdo-images.com/8X_4Y_2M_1K_5G_6C_7H_9=/fit-in/246x300/filters:strip_icc()/pic5786884.png",
    "La Isla Prohibida": "https://cf.geekdo-images.com/8X_4Y_2M_1K_5G_6C_7H_9=/fit-in/246x300/filters:strip_icc()/pic670845.jpg",
    "¡Aventureros al Tren!": "https://cf.geekdo-images.com/8X_4Y_2M_1K_5G_6C_7H_9=/fit-in/246x300/filters:strip_icc()/pic38668.jpg",
    "Carcassonne": "https://cf.geekdo-images.com/8X_4Y_2M_1K_5G_6C_7H_9=/fit-in/246x300/filters:strip_icc()/pic6544250.png",
    "Azul": "https://cf.geekdo-images.com/8X_4Y_2M_1K_5G_6C_7H_9=/fit-in/246x300/filters:strip_icc()/pic3718275.jpg",
    "Splendor": "https://cf.geekdo-images.com/8X_4Y_2M_1K_5G_6C_7H_9=/fit-in/246x300/filters:strip_icc()/pic1904079.jpg",
    "7 Wonders": "https://cf.geekdo-images.com/8X_4Y_2M_1K_5G_6C_7H_9=/fit-in/246x300/filters:strip_icc()/pic860217.jpg",
    "Catan": "https://cf.geekdo-images.com/8X_4Y_2M_1K_5G_6C_7H_9=/fit-in/246x300/filters:strip_icc()/pic2419375.jpg",
    "Root": "https://cf.geekdo-images.com/8X_4Y_2M_1K_5G_6C_7H_9=/fit-in/246x300/filters:strip_icc()/pic4254509.jpg",
    "Wingspan": "https://cf.geekdo-images.com/8X_4Y_2M_1K_5G_6C_7H_9=/fit-in/246x300/filters:strip_icc()/pic4458123.jpg"
}

def search_bgg(game_name):
    try:
        url = f'https://boardgamegeek.com/xmlapi2/search?query={urllib.parse.quote(game_name)}&type=boardgame&exact=1'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml = response.read()
        root = ET.fromstring(xml)
        for item in root.findall('item'):
            return item.get('id')
    except:
        pass
    return None

def get_bgg_image(game_id):
    try:
        url = f'https://boardgamegeek.com/xmlapi2/thing?id={game_id}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml = response.read()
        root = ET.fromstring(xml)
        for item in root.findall('item'):
            image = item.find('image')
            if image is not None:
                return image.text
    except:
        pass
    return "https://via.placeholder.com/246x300/011C6B/FFCC00?text=Juego"

result = []
for g in games:
    display_name = g.get('original', g['name'])
    image_url = preset_images.get(display_name)
    if not image_url:
        bgg_id = search_bgg(g['name'])
        if bgg_id:
            time.sleep(1.5) # respect rate limits
            image_url = get_bgg_image(bgg_id)
        else:
            image_url = f"https://via.placeholder.com/246x300/011C6B/FFCC00?text={urllib.parse.quote(display_name)}"
    
    g_final = {
        "name": display_name,
        "players": g['players'],
        "difficulty": g['difficulty'],
        "type": g['type'],
        "image": image_url
    }
    result.append(g_final)
    print(f"Processed {display_name}")

with open('games_with_images.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Done generating JSON")
