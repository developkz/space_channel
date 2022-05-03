import requests
from pathlib import Path
filepath = Path('images/HST-SM4.jpeg')
filepath.parent.mkdir(parents=True, exist_ok=True)

url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
response = requests.get(url)
response.raise_for_status()

with filepath.open('wb') as file:
    file.write(response.content)
