def create_auth_context(status, message, **kwargs):
    context = {
        'status': status,
        'message': message,
        **kwargs
    }
    return context


def telegram_share_url_generator(parameter):
    return f'https://t.me/share/url?url={parameter}'


def instagram_auth_url_generator():
    from flask import current_app
    config = current_app.config
    url = 'https://api.instagram.com/oauth/authorize' \
          f'?client_id={config["INSTAGRAM_CLIENT_ID"]}' \
          f'&redirect_uri={config["INSTAGRAM_AUTH_REDIRECT_URI"]}' \
          '&scope=user_profile,user_media' \
          '&response_type=code'
    return url
