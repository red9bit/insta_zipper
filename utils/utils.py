def create_auth_context(status, message, **kwargs):
    context = {
        'status': status,
        'message': message,
        **kwargs
    }
    return context


def telegram_share_url_generator(parameter):
    return f'https://t.me/share/url?url={parameter}'
