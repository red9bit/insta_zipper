import os

from celery import Celery
from zipfile import ZipFile

from zipper import instagram_api
from zipper import telegram_bot
from zipper.utils import download_and_save

app = Celery(
    'downloader',
    backend='rpc://',
    broker='pyamqp://guest@localhost//'
)


@app.task
def download_instagram_media(chat_id, user_id, long_lived_token):
    ok, res = instagram_api.query_the_user_media(long_lived_token, user_id)
    if not ok:
        # Log Here
        return

    data = res.json().get('data', [])
    if not data:
        # Log Here - user has no media on Instagram!
        return

    sub_directory = f'{chat_id}_{user_id}'

    route = f'media/{sub_directory}'
    if not os.path.exists(route):
        os.mkdir(route)

    zip_file_path = f'{route}/media.zip'
    zip_obj = ZipFile(zip_file_path, mode='w')

    media_counter = 0
    for item in data:
        media_id = item['id']
        media_url = item['media_url']

        print(media_url)

        media_path = download_and_save(media_url, route, media_id)
        if media_path:
            zip_obj.write(media_path)
        media_counter += 1

    zip_obj.close()

    msg = 'All Done!\n' \
          f'Number of downloaded media: {media_counter}\n' \
          'Your .zip file is on the way! Hang in there!!'
    telegram_bot.send_message(chat_id, msg)
    print('sending the document...')
    telegram_bot.send_document(chat_id, zip_file_path)
    print('completed!')
