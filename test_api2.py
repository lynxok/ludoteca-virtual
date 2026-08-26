import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
response = requests.get("https://boardgamegeek.com/xmlapi2/thing?id=13", headers=headers)
print(response.status_code)
if response.status_code == 200:
    print(response.text[:200])
else:
    print(response.text)
