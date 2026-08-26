import requests
import json
import os
import time
import re

with open('games_with_images.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

if not os.path.exists('portadas'):
    os.makedirs('portadas')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Referer': 'https://boardgamegeek.com/',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9,es;q=0.8'
}

print("Starting download utilizing requests...")
success_count = 0

for g in games:
    url = g['image']
    if 'via.placeholder.com' in url or 'http' not in url:
        continue
        
    safe_name = re.sub(r'[^\w\s-]', '', g['name']).strip().replace(' ', '_')
    ext = url.split('.')[-1]
    if len(ext) > 4 or '?' in ext:
        ext = 'jpg'
        
    local_filename = f"portadas/{safe_name}.{ext}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(local_filename, 'wb') as out_f:
                out_f.write(response.content)
            print(f"[{response.status_code}] Downloaded {safe_name}")
            success_count += 1
        else:
            print(f"[{response.status_code}] Failed {safe_name}")
            
    except Exception as e:
        print(f"Error {safe_name}: {e}")
        
    time.sleep(1.5) # BGGManager technique: pause to prevent bans

print(f"Finished! Successfully downloaded {success_count} real images.")
