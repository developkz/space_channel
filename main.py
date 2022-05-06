import os
from pathlib import Path

from dotenv import load_dotenv

import requests


def download_file(url: str, path: str) -> None:
    filename = os.path.basename(url)
    filepath = Path(f'{path}/{filename}')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()

    with filepath.open('wb') as file:
        file.write(response.content)


def fetch_spacex_launch():
    api_url = "https://api.spacexdata.com/v3/launches/65"

    payload = {}
    headers = {}

    space_x_answer = requests.request('GET', api_url, headers=headers, data=payload)
    return space_x_answer.json()['links']['flickr_images']


def download_spacex_launch_images():
    for url in fetch_spacex_launch():
        download_file(url, 'images')


def fetch_nasa_best_image(count: int = 1) -> list:
    api_url = "https://api.nasa.gov/planetary/apod"

    headers = {
        'api_key': nasa_token,
        'count': count
    }
    nasa_answer = requests.request('GET', api_url, params=headers)
    return nasa_answer.json()


def download_nasa_image(count: int = 1):
    for pic_of_day in fetch_nasa_best_image(count):
        download_file(pic_of_day['hdurl'], 'images')


# def fetch
if __name__ == '__main__':

    env_path = Path('.') / '.env'
    load_dotenv(env_path)
    nasa_token = os.getenv('NASA_API_KEY')

    download_nasa_image(3)

