import urllib.request
import json
import os
import re

with open('games_with_images.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

for g in games:
    url = g['image']
    if 'via.placeholder.com' in url or 'http' not in url:
        continue
    
    # Safe filename
    safe_name = re.sub(r'[^\w\s-]', '', g['name']).strip()
    ext = url.split('.')[-1]
    if len(ext) > 4:
        ext = 'jpg'
        
    local_filename = f"portadas/{safe_name}.{ext}"
    
    try:
        if not os.path.exists(local_filename):
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                with open(local_filename, 'wb') as out_f:
                    out_f.write(response.read())
        g['local_image'] = local_filename
        print(f"Downloaded {local_filename}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        g['local_image'] = url # fallback

with open('games_with_local_images.json', 'w', encoding='utf-8') as f:
    json.dump(games, f, ensure_ascii=False, indent=2)

print("Images downloaded and JSON updated")
