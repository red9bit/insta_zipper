def telegram_api_uri_generator(method_name):
    from flask import current_app
    config = current_app.config
    return config['TELEGRAM_BASE_URI'].format(
        token=config['TELEGRAM_BOT_TOKEN'],
        method_name=method_name
    )
