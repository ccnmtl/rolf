# flake8: noqa
from settings_shared import *
import os

# required settings:
SECRET_KEY = os.environ['SECRET_KEY']
API_SECRET = os.environ['API_SECRET']

# optional/defaulted settings
DB_NAME = os.environ.get('DB_NAME', 'rolf')
DB_HOST = os.environ.get(
    'DB_HOST', os.environ.get('POSTGRESQL_PORT_5432_TCP_ADDR', ''))
DB_PORT = int(os.environ.get(
    'DB_PORT', os.environ.get('POSTGRESQL_PORT_54342_TCP_PORT', 5432)))
DB_USER = os.environ.get('DB_USER', '')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')

AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN', None)
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', None)
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY', '')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY', '')
AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = AWS_SECRET_KEY

RAVEN_DSN = os.environ.get('RAVEN_DSN', '')

if 'ALLOWED_HOSTS' in os.environ:
    ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')

TIME_ZONE = os.environ.get('TIME_ZONE', 'America/New_York')

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', "rolf@ccnmtl.columbia.edu")

# -------------------------------------------

DEBUG = False
TEMPLATE_DEBUG = DEBUG

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',
        'NAME' : DB_NAME,
        'HOST' : DB_HOST,
        'PORT' : DB_PORT,
        'USER' : DB_USER,
        'PASSWORD' : DB_PASSWORD,
        }
}

if AWS_S3_CUSTOM_DOMAIN:
    AWS_PRELOAD_METADATA = True
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    S3_URL = 'https://%s/' % AWS_S3_CUSTOM_DOMAIN
    # static data, e.g. css, js, etc.
    STATICFILES_STORAGE = 'cacheds3storage.CompressorS3BotoStorage'
    STATIC_URL = 'https://%s/media/' % AWS_S3_CUSTOM_DOMAIN
    COMPRESS_ENABLED = True
    COMPRESS_OFFLINE = True
    COMPRESS_ROOT = STATIC_ROOT
    COMPRESS_URL = STATIC_URL
    COMPRESS_STORAGE = 'cacheds3storage.CompressorS3BotoStorage'

if RAVEN_DSN and 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')
    RAVEN_CONFIG = {
        'dsn': DSN,
    }
