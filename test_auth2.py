import requests

s = requests.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json'
})

payload = {
    "credentials": {
        "username": "Juansimon",
        "password": "Odin.1756"
    }
}
s.post("https://boardgamegeek.com/login/api/v1", json=payload)

# Test downloading an image
img_url = "https://cf.geekdo-images.com/rO7-vqwKvs47i27k1-B4FA__itemrep/img/bO6yq53q6q62Z0Q_0d_0jT_1wG8=/fit-in/246x300/filters:strip_icc()/pic2840020.jpg"
s.headers.update({'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8'})
r2 = s.get(img_url)
print("Image Status:", r2.status_code)
