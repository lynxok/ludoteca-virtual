import json
import os
import re
from PIL import Image, ImageDraw, ImageFont

with open('games_with_images.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

if not os.path.exists('portadas'):
    os.makedirs('portadas')

colors = [
    (1, 28, 107),   # bb-blue
    (150, 0, 50),   # dark red
    (0, 100, 0),    # dark green
    (100, 0, 100),  # purple
    (255, 100, 0),  # orange (dark)
]

def wrap_text(text, font, max_width, draw):
    lines = []
    words = text.split()
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        # Get length
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

try:
    font = ImageFont.truetype("arial.ttf", 30)
except:
    font = ImageFont.load_default()

for i, g in enumerate(games):
    safe_name = re.sub(r'[^\w\s-]', '', g['name']).strip().replace(' ', '_')
    local_filename = f"portadas/{safe_name}.jpg"
    
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
    g['local_image'] = local_filename

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

for g in games:
    g['image'] = g['local_image']

new_games_json_str = json.dumps(games, ensure_ascii=False, indent=4)
pattern = r'(const gamesData = )\[.*?\];'
html_new = re.sub(pattern, f"\\1{new_games_json_str};", html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_new)

print("Local generated images created.")
