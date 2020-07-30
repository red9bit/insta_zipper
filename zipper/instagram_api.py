from zipper.requests import request


def exchange_auth_code_for_token(auth_code):
    from flask import current_app
    config = current_app.config

    data = {
        'client_id': config['INSTAGRAM_CLIENT_ID'],
        'client_secret': config['INSTAGRAM_CLIENT_SECRET'],
        'redirect_uri': config['INSTAGRAM_AUTH_REDIRECT_URI'],
        'grant_type': 'authorization_code',
        'code': auth_code
    }

    ok, response = request(
        'https://api.instagram.com/oauth/access_token',
        method='POST',
        data=data
    )

    return ok, response


def exchange_token_for_long_lived_access_token(short_lived_token):
    from flask import current_app
    config = current_app.config

    query_params = {
        'client_secret': config['INSTAGRAM_CLIENT_SECRET'],
        'grant_type': 'ig_exchange_token',
        'access_token': short_lived_token
    }

    ok, response = request(
        'https://graph.instagram.com/access_token',
        params=query_params
    )

    return ok, response


def get_instagram_credential(auth_code):
    is_successful = False
    data = {
        'user_id': None,
        'access_token': None
    }

    ok, res = exchange_auth_code_for_token(auth_code)
    if not ok:
        return is_successful, data

    user_id = res.json().get('user_id')
    data['user_id'] = user_id

    short_lived_token = res.json().get('access_token')

    ok, res = exchange_token_for_long_lived_access_token(short_lived_token)
    if not ok:
        return is_successful, data

    access_token = res.json().get('access_token')
    data['access_token'] = access_token
    is_successful = True

    return is_successful, data


def query_the_user_media(long_lived_token, user_id):
    query_params = {
        'access_token': long_lived_token,
        'fields': 'id,media_type,media_url'
    }

    ok, response = request(
        f'https://graph.instagram.com/{user_id}/media',
        params=query_params
    )

    return ok, response
