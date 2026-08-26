import urllib.request
from bs4 import BeautifulSoup
import re

url = 'https://virtualvideostore.persona.co/'
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    
    print("TITLE:", soup.title.string if soup.title else "No title")
    print("\nBODY CLASSES:", soup.body.get('class', []))
    
    styles = soup.find_all('style')
    css_text = "\n".join([s.string for s in styles if s.string])
    
    # Print interesting CSS rules like backgrounds, grids, etc.
    print("\nSTYLES FOUND:")
    colors = set(re.findall(r'#[0-9a-fA-F]{3,6}', css_text))
    print("Colors:", colors)
    
    print("\nSTRUCTURE:")
    for tag in ['header', 'nav', 'main', 'footer', 'div']:
        elements = soup.find_all(tag, limit=3)
        for el in elements:
            print(f"<{tag} class='{el.get('class', [])}' id='{el.get('id', '')}'>")

    print("\nFirst few links:")
    for a in soup.find_all('a', limit=5):
        print(a.get('href'), a.get_text(strip=True))
except Exception as e:
    print("Error:", e)
