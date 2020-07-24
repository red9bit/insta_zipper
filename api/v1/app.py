from flask import Flask, request, render_template

from utils.utils import create_auth_context, telegram_share_url_generator

app = Flask(__name__)


@app.route('v1/auth')
def auth():
    auth_code = request.args.get('code')
    if not auth_code:
        context = create_auth_context(False, 'Something went wrong!')
        return render_template('instagram_callback.html', **context)

    clean_auth_code = auth_code[:-2]  # remove #_ from the end
    url = telegram_share_url_generator(clean_auth_code)
    message = 'Great! Please click on the link below and then select InstaZipper bot to continue...'
    context = create_auth_context(True, message, url=url)
    return render_template('instagram_callback.html', **context)


@app.route('/get_updates')
def get_updates():
    return
