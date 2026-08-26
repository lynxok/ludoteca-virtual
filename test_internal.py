import requests

s = requests.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'application/json, text/plain, */*'
})

payload = {
    "credentials": {
        "username": "Juansimon",
        "password": "Odin.1756"
    }
}
s.post("https://boardgamegeek.com/login/api/v1", json=payload)

# Query internal API for Catan
search_url = "https://boardgamegeek.com/api/search?q=catan"
r3 = s.get(search_url)
print("Search Status:", r3.status_code)
if r3.status_code == 200:
    data = r3.json()
    if 'items' in data and len(data['items']) > 0:
        item = data['items'][0]
        print("Name:", item.get('name'))
        print("Image URL:", item.get('imageurl'))
