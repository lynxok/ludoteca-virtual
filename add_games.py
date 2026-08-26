import json
import os
import re
import random
from PIL import Image, ImageDraw, ImageFont

new_games = [
    "Catan ciudades y caballeros",
    "Catan Energias renovables",
    "Melomano",
    "Panic Lab",
    "Atenea",
    "Bleef",
    "Jardin japones",
    "Count up",
    "Equipazo",
    "Munchkin: Dragones molones",
    "Munchkin 3: Errores clericales",
    "Munchkin 7: Trampas a dos manos",
    "Camarero",
    "CACA"
]

with open('games_with_images.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

# Add rating to existing games if not present
for g in games:
    if 'rating' not in g:
        g['rating'] = str(round(random.uniform(6.5, 9.0), 1))

# Append new games
for ng in new_games:
    safe_name = re.sub(r'[^\w\s-]', '', ng).strip().replace(' ', '_')
    local_image = f"portadas/{safe_name}.jpg"
    games.append({
        "name": ng,
        "players": "2-6",
        "difficulty": "Media",
        "type": "Expansión / Cartas",
        "rating": str(round(random.uniform(6.0, 8.5), 1)),
        "image": local_image,
        "local_image": local_image
    })

with open('games_with_images.json', 'w', encoding='utf-8') as f:
    json.dump(games, f, ensure_ascii=False, indent=2)

# Generate placeholders for new games
colors = [(1, 28, 107), (150, 0, 50), (0, 100, 0), (100, 0, 100), (255, 100, 0)]
try:
    font = ImageFont.truetype("arial.ttf", 30)
except:
    font = ImageFont.load_default()

def wrap_text(text, font, max_width, draw):
    lines = []
    words = text.split()
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

for i, g in enumerate(games):
    local_filename = g['local_image']
    if not os.path.exists(local_filename):
        img = Image.new('RGB', (246, 300), color=colors[i % len(colors)])
        d = ImageDraw.Draw(img)
        lines = wrap_text(g['name'], font, 220, d)
        y_text = 100
        for line in lines:
            bbox = d.textbbox((0, 0), line, font=font)
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            d.text(((246 - width) / 2, y_text), line, fill=(255, 255, 255), font=font)
            y_text += height + 10
        img.save(local_filename)

print("Games updated and images generated.")
