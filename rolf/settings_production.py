# flake8: noqa
from settings_shared import *

TEMPLATE_DIRS = (
    "/var/www/rolf/rolf/rolf/templates",
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

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

try:
    from local_settings import *
except ImportError:
    pass

try:
    INSTALLED_APPS += LOCAL_INSTALLED_APPS
except:
    pass
