import json
import re

with open('games_with_images.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

for g in games:
    g['image'] = g['local_image']

new_games_json_str = json.dumps(games, ensure_ascii=False, indent=4)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = r'(const gamesData = )\[.*?\];'
html_new = re.sub(pattern, f"\\1{new_games_json_str};", html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_new)
