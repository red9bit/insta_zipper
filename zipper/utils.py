import requests
import os


def telegram_api_uri_generator(method_name):
    from flask import current_app
    config = current_app.config
    return config['TELEGRAM_BASE_URI'].format(
        token=config['TELEGRAM_BOT_TOKEN'],
        method_name=method_name
    )


def download_and_save(url, route, file_name):
    path = f'{route}/{file_name}'
    if not os.path.exists(path):
        print('Download for url: %s started!' % url)
        response = requests.get(url)
        open(path, 'wb').write(response.content)
        print('Download completed!')
        return path
    else:
        print('%s is already exists!' % url)
        return None
