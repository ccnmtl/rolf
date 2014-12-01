import os, sys, site

# enable the virtualenv
site.addsitedir('/var/www/rolf/rolf/ve/lib/python2.7/site-packages')

# paths we might need to pick up the project's settings
sys.path.append('/var/www/rolf/rolf/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'rolf.settings_production'

import django
django.setup()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
