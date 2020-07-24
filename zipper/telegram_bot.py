from zipper.requests import request
from .utils import telegram_api_uri_generator


def send_message(chat_id, text):
    data = {
        'chat_id': chat_id,
        'text': text
    }
    ok, _ = request(
        telegram_api_uri_generator('sendMessage'),
        method='POST',
        data=data
    )

    if ok:
        print('Message has been sent to the user')
    else:
        print('Could not send the message to user! something went wrong!')
