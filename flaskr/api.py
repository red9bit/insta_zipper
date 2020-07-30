import datetime

from flask import Blueprint, render_template, request, current_app as app

from zipper.tasks import download_instagram_media
from zipper.telegram_bot import send_message
from zipper.instagram_api import get_instagram_credential

from utils.utils import connect_to_mongodb
from .utils import create_auth_context, telegram_share_url_generator, instagram_auth_url_generator

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/auth', methods=['GET'])
def instagram_authenticate():
    auth_code = request.args.get('code')
    if auth_code:
        clean_auth_code = auth_code.split('#_')[0]  # remove #_ from the end
        url = telegram_share_url_generator(clean_auth_code)
        message = 'Great! Please click on the link below and then select InstaZipper bot to continue...'
        context = create_auth_context(True, message, url=url)

        # write Instagram auth code into MongoDB
        client, db = connect_to_mongodb()
        instagram_auth_collection = db[app.config['COLLECTION_INSTAGRAM_AUTH_CODES']]
        instagram_auth_collection.insert_one({
            'date_stats': datetime.datetime.now(),
            'source_ip': request.remote_addr,
            'auth_code': clean_auth_code,
        })
        client.close()
    else:
        context = create_auth_context(False, 'Something went wrong!')
    return render_template('api/instagram_callback.html', **context)


@bp.route('/get_updates', methods=['POST'])
def get_telegram_updates():
    data = request.json
    message = data.get('message', data.get('edited_message'))
    text = message.get('text').strip()
    chat_id = message['chat']['id']

    client, db = connect_to_mongodb()

    # try fetching Telegram chat from MongoDB
    telegram_chat_collection = db[app.config['COLLECTION_TELEGRAM_CHATS']]
    telegram_chat_record = telegram_chat_collection.find_one({
        'chat_id': chat_id
    })

    if text == '/start':
        if telegram_chat_record:
            msg = 'Oops! You already being introduced!'
            send_message(chat_id, msg)
        else:
            msg = 'Hello and welcome to InstaZipper!\n' \
                  'Click on the following link and then login to your Instagram account to continue...'
            send_message(chat_id, msg)
            send_message(chat_id, instagram_auth_url_generator())
    elif text == '/login_url':
        if telegram_chat_record:
            msg = 'You already logged in to your Instagram account!\n' \
                  'You can use `/get_zip` to get a zip archive from all of your media.'
            send_message(chat_id, msg)
        else:
            msg = 'Oh, sure! Here you are'
            send_message(chat_id, msg)
            send_message(chat_id, instagram_auth_url_generator())
    elif text == '/get_zip':
        if not telegram_chat_record:
            msg = 'You must login to your Instagram account first in order to get a zip file from your media!\n' \
                  'Try using `/login_url` to login to your Instagram account.'
            send_message(chat_id, msg)
        else:
            msg = 'Download has been started!\n' \
                  'Please wait...'
            send_message(chat_id, msg)
            download_instagram_media(
                chat_id,
                telegram_chat_record['instagram_user_id'],
                telegram_chat_record['token']
            )
    else:
        # try fetching Instagram auth code from MongoDB
        instagram_auth_collection = db[app.config['COLLECTION_INSTAGRAM_AUTH_CODES']]
        instagram_auth_record = instagram_auth_collection.find_one({
            'auth_code': text
        })
        if not instagram_auth_record:
            msg = 'Oops! Looks like something went wrong!\n' \
                  'Please try login to your Instagram account first, and then send the valid AUTH token ' \
                  'or use one of the valid commands!\n\n' \
                  'You can use `/login_url` to get an Instagram login URL.'
            send_message(chat_id, msg)
        else:
            auth_code = text
            ok, data = get_instagram_credential(auth_code)
            if not ok:
                msg = 'Oh! something is wrong!\n' \
                      'Please try again later...'
                send_message(chat_id, msg)
            else:
                telegram_chat_collection.insert_one({
                    'add_time': datetime.datetime.now(),
                    'chat_id': chat_id,
                    'instagram_user_id': data['user_id'],
                    'auth_code': text,
                    'token': data['access_token']
                })
                msg = 'Well done!\n' \
                      'You are now logged in to your Instagram account.\n' \
                      'What are you waiting for?! Lets use `/get_zip` to get a zip archive from all of your media!'
                send_message(chat_id, msg)

    client.close()
    return {}, 200
