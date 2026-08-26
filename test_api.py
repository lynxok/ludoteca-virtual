import requests

headers = {
    'User-Agent': 'Antigravity/1.0 (Testing API access for private local app)'
}
response = requests.get("https://boardgamegeek.com/xmlapi2/thing?id=13", headers=headers)
print(response.status_code)
if response.status_code == 200:
    print(response.text[:500])
else:
    print(response.text)
