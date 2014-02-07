# Django settings for rolf project.
import os.path
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

ALLOWED_HOSTS = ['.ccnmtl.columbia.edu', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rolf',
        'HOST': '',
        'PORT': 5432,
        'USER': '',
        'PASSWORD': '',
    }
}

if 'test' in sys.argv or 'jenkins' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
        }
    }

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SOUTH_TESTS_MIGRATE = False

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=rolf.rolf_main',
]

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
)

PROJECT_APPS = ['rolf.rolf_main', ]

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = "/var/www/rolf/uploads/"
MEDIA_URL = '/uploads/'
ADMIN_MEDIA_PREFIX = '/media/'
STATIC_URL = "/media/"
SECRET_KEY = 'OVERRIDE THIS IN YOUR local_settings.py'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'rolf.rolf_main.context_processors.wind_settings',
)

MIDDLEWARE_CLASSES = (
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'rolf.urls'

TEMPLATE_DIRS = (
    "/var/www/rolf/templates/",
    os.path.join(os.path.dirname(__file__), "templates"),
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'django.contrib.admin',
    'django_extensions',
    'munin',
    'rolf.rolf_main',
    'django_statsd',
    'south',
    'raven.contrib.django',
    'smoketest',
    'debug_toolbar',
    'django_jenkins',
]

INTERNAL_IPS = ('127.0.0.1', )
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

STATSD_CLIENT = 'statsd.client'
STATSD_PREFIX = 'rolf'
STATSD_HOST = 'localhost'
STATSD_PORT = 8125
if 'test' in sys.argv or 'jenkins' in sys.argv:
    STATSD_HOST = '127.0.0.1'

STATSD_PATCHES = ['django_statsd.patches.db', ]

EMAIL_SUBJECT_PREFIX = "[rolf] "
EMAIL_HOST = 'localhost'
SERVER_EMAIL = "rolf@yoursite.com"


CHECKOUT_DIR = "/var/tmp/rolf/checkouts/"
SCRIPT_DIR = "/var/tmp/rolf/scripts/"
if 'test' in sys.argv or 'jenkins' in sys.argv:
    import tempfile
    base = tempfile.gettempdir()
    CHECKOUT_DIR = os.path.join(base, "checkouts/")
    try:
        os.makedirs(CHECKOUT_DIR)
    except:
        pass
    SCRIPT_DIR = os.path.join(base, "scripts/")
    try:
        os.makedirs(SCRIPT_DIR)
    except:
        pass

API_SECRET = "YOU MUST SET THIS IN A local_settings.py FILE"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}
