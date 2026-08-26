import requests
import xml.etree.ElementTree as ET

s = requests.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})

payload = {
    "credentials": {
        "username": "Juansimon",
        "password": "Odin.1756"
    }
}
s.post("https://boardgamegeek.com/login/api/v1", json=payload)

# Query XML API for Catan (ID 13)
xml_url = "https://boardgamegeek.com/xmlapi2/thing?id=13"
r3 = s.get(xml_url)
print("XML Status:", r3.status_code)
if r3.status_code == 200:
    root = ET.fromstring(r3.content)
    img_element = root.find('.//image')
    if img_element is not None:
        raw_img_url = img_element.text
        print("Raw Image URL:", raw_img_url)
        # Try to download it
        r4 = s.get(raw_img_url)
        print("Raw Image Download Status:", r4.status_code)
