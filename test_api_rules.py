import requests

r = requests.get("https://boardgamegeek.com/using_the_xml_api", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
print(r.status_code)
from bs4 import BeautifulSoup
try:
    soup = BeautifulSoup(r.text, 'html.parser')
    for p in soup.find_all('p'):
        print(p.text)
except:
    print("bs4 not found")
