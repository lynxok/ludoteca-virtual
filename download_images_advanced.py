import urllib.request
import json
import os
import re
import time

with open('games_with_images.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

if not os.path.exists('portadas'):
    os.makedirs('portadas')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Referer': 'https://boardgamegeek.com/',
    'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

for g in games:
    url = g['image']
    if 'via.placeholder.com' in url or 'http' not in url:
        g['local_image'] = "portadas/default.jpg"
        continue
        
    safe_name = re.sub(r'[^\w\s-]', '', g['name']).strip().replace(' ', '_')
    ext = url.split('.')[-1]
    if len(ext) > 4 or '?' in ext:
        ext = 'jpg'
        
    local_filename = f"portadas/{safe_name}.{ext}"
    
    if not os.path.exists(local_filename):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                with open(local_filename, 'wb') as out_f:
                    out_f.write(response.read())
            print(f"Downloaded {local_filename}")
            time.sleep(0.5) # Be nice to the server
        except Exception as e:
            print(f"Failed {safe_name}: {e}")
            local_filename = url # fallback
    else:
        print(f"Already exists {local_filename}")
        
    g['local_image'] = local_filename

# Update index.html directly
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the gamesData block in HTML
import json
games_json_str = json.dumps(games, ensure_ascii=False, indent=4)
# Make sure to replace the image field with local_image inside the JS payload
# Actually, let's just modify the JSON structure before dumping
for g in games:
    g['image'] = g['local_image']

new_games_json_str = json.dumps(games, ensure_ascii=False, indent=4)

# Regex to replace the gamesData array in index.html
pattern = r'(const gamesData = )\[.*?\];'
html_new = re.sub(pattern, f"\\1{new_games_json_str};", html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_new)

print("HTML updated with local image paths.")
