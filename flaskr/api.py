import datetime

from flask import Blueprint, render_template, request, current_app as app
from zipper.telegram_bot import send_message

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

    if text == '/start':
        msg = 'Hello and welcome to InstaZipper!\n' \
              'Click on the following link and then login to your Instagram account to continue...'
        send_message(chat_id, msg)
        send_message(chat_id, instagram_auth_url_generator())
    else:
        pass

    return {}, 200
