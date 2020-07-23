from flask import Flask, request
from .utils import create_auth_response

app = Flask(__name__)


@app.route('/auth')
def auth():
    auth_code = request.args.get('code')
    if not auth_code:
        return create_auth_response(False, '`code` query param does not exist'), 400
    return create_auth_response(True, 'success', code=auth_code), 200


@app.route('/get_updates')
def get_updates():
    return
