from flask import Blueprint, render_template, request
from .utils import create_auth_context, telegram_share_url_generator

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/auth', methods=['GET'])
def instagram_authenticate():
    auth_code = request.args.get('code')
    if auth_code:
        clean_auth_code = auth_code[:-2]  # remove #_ from the end
        url = telegram_share_url_generator(clean_auth_code)
        message = 'Great! Please click on the link below and then select InstaZipper bot to continue...'
        context = create_auth_context(True, message, url=url)
    else:
        context = create_auth_context(False, 'Something went wrong!')
    return render_template('api/instagram_callback.html', **context)


@bp.route('/get_updates', methods=['GET'])
def get_updates():
    return
