import os
from pathlib import Path

import requests


def download_file(url: str, path: str) -> None:
    filename = os.path.basename(url)
    filepath = Path(f'{path}/{filename}')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()

    with filepath.open('wb') as file:
        file.write(response.content)


api_url = "https://api.spacexdata.com/v3/launches/67"

payload = {}
headers = {}

space_x_answer = requests.request("GET", api_url, headers=headers, data=payload)

response_dict = space_x_answer.json()
images_links_list = response_dict['links']['flickr_images']

for i in images_links_list:
    download_file(i, 'images')

# download_file('https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg', 'images')
