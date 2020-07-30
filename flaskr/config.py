from decouple import config
from utils.utils import str_or_none_cast

# Development
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY', cast=str)

# MongoDB
MONGO_HOST = config('MONGO_HOST', cast=str)
MONGO_DB = config('MONGO_DB', cast=str)
MONGO_USER = config('MONGO_USER', cast=str_or_none_cast)
MONGO_PASS = config('MONGO_PASS', cast=str_or_none_cast)

# MongoDB collections
COLLECTION_INSTAGRAM_AUTH_CODES = config('COLLECTION_INSTAGRAM_AUTH_CODES', default='instagram_auth_codes', cast=str)
COLLECTION_TELEGRAM_CHATS = config('COLLECTION_TELEGRAM_CHATS', default='telegram_chats', cast=str)

# Celery Broker
CELERY_BROKER_HOST = config('CELERY_BROKER_HOST', cast=str)
CELERY_BROKER_USER = config('CELERY_BROKER_USER', cast=str)
CELERY_BROKER_PASS = config('CELERY_BROKER_PASS', cast=str)
CELERY_BROKER_URL = f'amqp://{CELERY_BROKER_USER}:{CELERY_BROKER_PASS}@{CELERY_BROKER_HOST}'

# Instagram configs
INSTAGRAM_AUTH_REDIRECT_URI = config('INSTAGRAM_AUTH_REDIRECT_URI', cast=str)
INSTAGRAM_CLIENT_ID = config('INSTAGRAM_CLIENT_ID', cast=str)
INSTAGRAM_CLIENT_SECRET = config('INSTAGRAM_CLIENT_SECRET', cast=str)

# Telegram configs
TELEGRAM_BASE_URI = 'https://api.telegram.org/bot{token}/{method_name}'
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN', cast=str)
