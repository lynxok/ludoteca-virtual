import requests

s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0'})
r = s.post("https://boardgamegeek.com/login/api/v1", json={"credentials": {"username": "test", "password": "test"}})
print(r.status_code)
print(r.text[:200])
