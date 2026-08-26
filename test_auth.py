import requests

s = requests.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json'
})

payload = {
    "credentials": {
        "username": "Juansimon",
        "password": "Odin.1756"
    }
}

print("Attempting login...")
r = s.post("https://boardgamegeek.com/login/api/v1", json=payload)
print("Status:", r.status_code)
print("Response:", r.text)
