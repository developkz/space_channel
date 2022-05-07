import os
from pathlib import Path
from pprint import pprint

from datetime import datetime

from urllib.parse import urlparse
from dotenv import load_dotenv

import requests


def download_file(url: str, path: str) -> None:
    file_path = urlparse(url).path
    filename = os.path.basename(file_path)
    filesystem_path = Path(f'{path}/{filename}')
    filesystem_path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()

    with filesystem_path.open('wb') as file:
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


def fetch_nasa_natural_earth():
    api_url = 'https://api.nasa.gov/EPIC/api/natural/'

    headers = {
        'api_key': nasa_token,
    }
    nasa_answer = requests.request('GET', api_url, params=headers)
    urls_to_images = []
    for item in nasa_answer.json():
        date_of_image = datetime.strptime(item['date'], '%Y-%m-%d  %H:%M:%S')
        image_name = item['image']
        urls_to_images.append(
            f'https://api.nasa.gov/EPIC/archive/natural/{date_of_image.year}/{"{:02d}".format(date_of_image.month)}/{"{:02d}".format(date_of_image.day)}/png/{image_name}.png?api_key=DEMO_KEY')
    return urls_to_images


def download_nasa_natural_image(count: int = 1):
    urls_list = fetch_nasa_natural_earth()
    # pprint(urls_list)
    for url in urls_list[:count]:
        download_file(url, 'images')


if __name__ == '__main__':
    env_path = Path('.') / '.env'
    load_dotenv(env_path)
    nasa_token = os.getenv('NASA_API_KEY')
    # fetch_nasa_natural_earth(2)
    # download_nasa_image(3)
    download_nasa_natural_image(4)
