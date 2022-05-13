# NASA images Telegram poster.

Скрипт в автоматическом режиме скачивает нужное количество изображений и публикует их
в необходимом телеграм канале через бота. 

## Настройка виртуального окружения
Скопируйте или клонируйте этот репозиторий себе на компьютер.

Войдите в папку проекта и создайте виртуальное окружение.

```shell
python3 -m venv env  #создание окружения
source env/bin/activate  #активация виртуального окружения
```

Для того чтобы установить необходимые модули запустите команду:

```shell
pip install -r requirements.txt
```

## Настройка токенов доступа

Переименуйте `.env.sample` в `.env`

Установите все необходимые модули.

```shell
python3 -m pip install requirements.txt
```

Для получения NASA_API_KEY перейдите по ссылке [Nasa Generate API](https://api.nasa.gov/) и следуйте инструкциям.
Для регистрации бота и получения токена воспользуйтесь ссылкой [Telegram Botfather Guide](https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot)
Для создания объекта bot воспользуйтесь этим руководством [Как отправить сообщение в группу](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API)

```venv
NASA_API_KEY=<Paste your token here>
TELEGRAM_API_KEY=<Paste your token here>
TELEGRAM_CHAT_ID=<Paste chat id here>

NASA_BEST_IMAGES_TO_DOWNLOAD=1  #количество загружаемых изображений из NASA Best Images
NASA_NATURAL_IMAGES_TO_DOWNLOAD=1  #количество загружаемых изображений из NASA Natural Earth
SPACEX_LAUNCH_IMAGES_TO_DOWNLOAD=1  #количество загружаемых изображений из запуска Spacex

TIME_SLEEP=86400  #day 86400-seconds
```

После успешного запуска и постинга картинок они автоматически удалятся из папки images.

Пример успешного запуска скрипта:

```text
Attempt 1... STARTED!
Fetching and downloading images to "images/"
Images downloading... OK!
Posting images...
Images Posting... OK!
Images Deleting...
Images Deleting... OK!
Started sleep for 86400 seconds...
```
