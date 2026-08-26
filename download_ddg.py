import urllib.request
import json
import os
import re
import time
from duckduckgo_search import DDGS

with open('games_with_images.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

if not os.path.exists('portadas'):
    os.makedirs('portadas')

def download_image(url, filename):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(filename, 'wb') as out_f:
                out_f.write(response.read())
        return True
    except:
        return False

ddgs = DDGS()

for g in games:
    safe_name = re.sub(r'[^\w\s-]', '', g['name']).strip().replace(' ', '_')
    local_filename = f"portadas/{safe_name}.jpg"
    
    if not os.path.exists(local_filename):
        print(f"Searching for {g['name']}...")
        try:
            results = list(ddgs.images(f"{g['name']} board game box cover", max_results=3))
            downloaded = False
            for res in results:
                if download_image(res['image'], local_filename):
                    print(f"Downloaded {local_filename}")
                    downloaded = True
                    break
            if not downloaded:
                print(f"Failed to download {g['name']}")
        except Exception as e:
            print(f"Error searching {g['name']}: {e}")
        time.sleep(1) # Be nice
    else:
        print(f"Already exists {local_filename}")
        
    g['local_image'] = local_filename

# Update index.html directly
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

for g in games:
    g['image'] = g['local_image']

new_games_json_str = json.dumps(games, ensure_ascii=False, indent=4)
pattern = r'(const gamesData = )\[.*?\];'
html_new = re.sub(pattern, f"\\1{new_games_json_str};", html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_new)

print("Images downloaded via DDG and HTML updated.")
