from settings_shared import *

TEMPLATE_DIRS = (
    "/var/www/rolf/rolf/templates",
)

MEDIA_ROOT = '/var/www/rolf/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/rolf/rolf/sitemedia')
)


DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rolf',
        'HOST': '',
        'PORT': 6432,
        'USER': '',
        'PASSWORD': '',
        }
}

SENTRY_SITE = 'rolf'
SENTRY_SERVERS = ['http://sentry.ccnmtl.columbia.edu/sentry/store/']

import logging
from raven.contrib.django.handlers import SentryHandler
logger = logging.getLogger()
# ensure we havent already registered the handler
if SentryHandler not in map(type, logger.handlers):
    logger.addHandler(SentryHandler())

    # Add StreamHandler to sentry's default so you can catch missed exceptions
    logger = logging.getLogger('sentry.errors')
    logger.propagate = False
    logger.addHandler(logging.StreamHandler())


try:
    from local_settings import *
except ImportError:
    pass

try:
    INSTALLED_APPS += LOCAL_INSTALLED_APPS
except:
    pass
