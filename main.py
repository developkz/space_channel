import os
import shutil
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

import requests

import telegram


def download_file(url: str, path: str) -> None:
    """Скачивает файл из адреса url в указанный путь path."""
    path_to_file = urlparse(url).path
    file_name = os.path.basename(path_to_file)
    path_to_save_images = Path(f'{path}/{file_name}')
    path_to_save_images.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()

    with path_to_save_images.open('wb') as file:
        file.write(response.content)


def fetch_spacex_launch(launch_number: int = 67):
    """Возвращает список ссылок на изображения с запуска SpaceX №67."""
    api_url = f"https://api.spacexdata.com/v3/launches/{launch_number}"

    space_x_answer = requests.request('GET', api_url)
    space_x_answer.raise_for_status()
    return space_x_answer.json()


def fetch_nasa_best_image(token: str, count: int = 1):
    """Получает count ссылок на лучшие изображения дня,
    NASA 'A Picture Of the Day'."""
    api_url = "https://api.nasa.gov/planetary/apod"

    headers = {
        'api_key': token,
        'count': count
    }
    try:
        nasa_answer = requests.request('GET', api_url, params=headers)
        nasa_answer.raise_for_status()
        return nasa_answer.json()
    except requests.exceptions.HTTPError:
        return None


def fetch_nasa_natural_earth(token: str) -> list:
    """Возвращает ссылки на изображения Natural Earth NASA."""
    api_url = 'https://api.nasa.gov/EPIC/api/natural/'

    headers = {
        'api_key': token,
    }
    nasa_answer = requests.request('GET', api_url, params=headers)
    nasa_answer.raise_for_status()
    urls_to_images = []
    for item in nasa_answer.json():
        parsed_date = datetime.strptime(item['date'], '%Y-%m-%d  %H:%M:%S')
        date = f'{parsed_date.year}/{"{:02d}".format(parsed_date.month)}/{"{:02d}".format(parsed_date.day)}'
        image_name = item['image']
        urls_to_images.append(f'https://api.nasa.gov/EPIC/archive/natural/{date}/png/{image_name}.png')
    return urls_to_images


def download_nasa_image(token: str, count: int = 1) -> None:
    """Загружает count изображения из NASA 'A Picture Of the Day'."""
    for pic_of_day in fetch_nasa_best_image(token, count):
        download_file(pic_of_day['hdurl'] or pic_of_day['url'], 'images')


def download_nasa_natural_image(path_to_save,
                                api_key: str,
                                token: str,
                                count: int = 1):
    """Загружает count ссылок из списка
    fetch_nasa_natural_earth() ссылок."""
    urls = fetch_nasa_natural_earth(token)
    os.makedirs(os.path.dirname(f'{path_to_save}/'), exist_ok=True)
    for url in urls[:count]:
        file_name = os.path.basename(url)
        params = {
            'api_key': api_key
        }
        image = requests.get(url, params=params)
        if image.status_code == 200:
            open(file_name, 'wb').write(image.content)
            os.rename(file_name, f'{path_to_save}/{file_name}')


def download_spacex_launch_images(count: int = 0,
                                  launch_number: int = 67):
    """Загружает count изображений из запуска launch_number SpaceX."""
    images_of_launch_urls_list = fetch_spacex_launch(launch_number)['links']['flickr_images']
    if count >= len(images_of_launch_urls_list):
        for url in images_of_launch_urls_list:
            download_file(url, 'images')
    else:
        for url in images_of_launch_urls_list[:count]:
            download_file(url, 'images')


def post_telegram_image(path: Path) -> None:
    """Публикует изображения из директории в
    канал телеграм через телеграм бота."""
    for root, directory, files in os.walk(path):
        for file in files:
            bot.sendPhoto(photo=open(f'{path}/{file}', 'rb'),
                          chat_id=telegram_channel_id,
                          timeout=150)


if __name__ == '__main__':

    env_path = Path('.') / '.env'
    load_dotenv(env_path)

    nasa_token = os.getenv('NASA_API_KEY')
    nasa_api_key = os.getenv('NASA_DEMO_API_KEY')
    telegram_token = os.getenv('TELEGRAM_API_KEY')
    telegram_channel_id = os.getenv('TELEGRAM_CHAT_ID')
    time_sleep = int(os.getenv('TIME_SLEEP'))
    best_images_count = int(os.getenv('NASA_BEST_IMAGES_TO_DOWNLOAD'))
    natural_images_count = int(os.getenv('NASA_NATURAL_IMAGES_TO_DOWNLOAD'))
    spacex_launches_count = int(os.getenv('SPACEX_LAUNCH_IMAGES_TO_DOWNLOAD'))
    bot = telegram.Bot(telegram_token)
    images_path = Path('images/')
    post_attempt = 1

    while True:

        print(f'Attempt {post_attempt}... STARTED!')
        print(f'Fetching and downloading images to "{images_path}/"')

        download_nasa_image(nasa_token, best_images_count)
        download_nasa_natural_image(images_path, nasa_api_key, nasa_token)
        download_spacex_launch_images(spacex_launches_count)

        print('Images downloading... OK!')
        print('Images posting...')

        post_telegram_image(images_path)

        print('Images Posting... OK!')

        time.sleep(2)

        print(f'Images Deleting...')

        time.sleep(2)
        shutil.rmtree(images_path)

        print(f'Images Deleting... OK!')

        post_attempt += 1

        print(f'Started sleep for {time_sleep} seconds...')

        time.sleep(time_sleep)
