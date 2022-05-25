import asyncio
import os
import shutil
from datetime import datetime
from pathlib import Path
from pprint import pprint
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


def fetch_spacex_launch(launch_number: int = 67) -> list:
    """Возвращает список ссылок на изображения с запуска SpaceX №67."""
    api_url = f"https://api.spacexdata.com/v3/launches/{launch_number}"

    space_x_answer = requests.request('GET', api_url)
    space_x_answer.raise_for_status()
    return space_x_answer.json()['links']['flickr_images']


def download_spacex_launch_images(count: int = 0, launch_number: int = 0):
    """Загружает count изображений из запуска launch_number SpaceX."""
    images_of_launch_urls_list = fetch_spacex_launch(launch_number)
    if count >= len(images_of_launch_urls_list):
        for url in images_of_launch_urls_list:
            download_file(url, 'images')
    else:
        for url in images_of_launch_urls_list[:count]:
            download_file(url, 'images')


def fetch_nasa_best_image(count: int = 1):
    """Получает count ссылок на лучшие изображения дня, NASA 'A Picture Of the Day'."""
    api_url = "https://api.nasa.gov/planetary/apod"

    headers = {
        'api_key': nasa_token,
        'count': count
    }
    try:
        nasa_answer = requests.request('GET', api_url, params=headers)
        nasa_answer.raise_for_status()
        return nasa_answer.json()
    except requests.exceptions.HTTPError:
        return None


def download_nasa_image(count: int = 1) -> None:
    """Загружает count изображения из NASA 'A Picture Of the Day'."""
    for pic_of_day in fetch_nasa_best_image(count):
        download_file(pic_of_day['hdurl'] or pic_of_day['url'], 'images')


def fetch_nasa_natural_earth() -> list:
    """Возвращает ссылки на изображения Natural Earth NASA."""
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
            f'https://api.nasa.gov/EPIC/archive/natural/{date_of_image.year}/'
            f'{"{:02d}".format(date_of_image.month)}/'
            f'{"{:02d}".format(date_of_image.day)}'
            f'/png/{image_name}.png?api_key=DEMO_KEY'
        )
    return urls_to_images


def download_nasa_natural_image(count: int = 1) -> None:
    """Загружает count ссылок из списка fetch_nasa_natural_earth() ссылок."""
    urls_list = fetch_nasa_natural_earth()
    # pprint(urls_list)
    for url in urls_list[:count]:
        download_file(url, 'images')


async def post_telegram_image(path: str) -> None:
    """Публикует изображения из директории в канал телеграм через телеграм бота."""
    for root, directory, files in os.walk(path):
        for file in files:
            bot.sendPhoto(photo=open(f'{path}/{file}', 'rb'),
                          chat_id=telegram_channel_id,
                          timeout=150)


async def sleep_for_time(sleep: int) -> None:
    """Sleep Time"""
    await asyncio.sleep(sleep)


def delete_files(source: str) -> None:
    """Удаляет директорию Path(source)"""
    shutil.rmtree(source)


if __name__ == '__main__':

    env_path = Path('.') / '.env'
    load_dotenv(env_path)

    nasa_token = os.getenv('NASA_API_KEY')
    telegram_token = os.getenv('TELEGRAM_API_KEY')
    telegram_channel_id = os.getenv('TELEGRAM_CHAT_ID')
    time_sleep = int(os.getenv('TIME_SLEEP'))
    best_images_count = int(os.getenv('NASA_BEST_IMAGES_TO_DOWNLOAD'))
    natural_images_count = int(os.getenv('NASA_NATURAL_IMAGES_TO_DOWNLOAD'))
    spacex_launches_count = int(os.getenv('SPACEX_LAUNCH_IMAGES_TO_DOWNLOAD'))
    bot = telegram.Bot(telegram_token)
    images_path = Path('images/')
    post_attempt = 1

    # download_spacex_launch_images(23, 56)
    pprint(fetch_nasa_best_image())
    # while True:
    #     print(f'Attempt {post_attempt}... STARTED!')
    #     print(f'Fetching and downloading images to "{images_path}/"')
    #
    #     download_nasa_image(best_images_count)
    #     download_nasa_natural_image(natural_images_count)
    #     download_spacex_launch_images(spacex_launches_count)
    #
    #     print('Images downloading... OK!')
    #     print('Images posting...')
    #
    #     asyncio.run(post_telegram_image(images_path))
    #
    #     print('Images Posting... OK!')
    #
    #     asyncio.run(sleep_for_time(2))
    #
    #     print(f'Images Deleting...')
    #
    #     asyncio.run(sleep_for_time(2))
    #     delete_files(images_path)
    #
    #     print(f'Images Deleting... OK!')
    #
    #     post_attempt += 1
    #
    #     print(f'Started sleep for {time_sleep} seconds...')
    #
    #     asyncio.run(sleep_for_time(time_sleep))
