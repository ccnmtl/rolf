# Django settings for rolf project.
import os.path
import sys
from ccnmtlsettings.shared import common

project = 'rolf'
base = os.path.dirname(__file__)

locals().update(
    common(
        project=project,
        base=base,
    )
)

PROJECT_APPS = ['rolf.rolf_main', ]

INSTALLED_APPS += [  # noqa
    'rolf.rolf_main',
]

WIND_AFFIL_HANDLERS = ['whitelistaffilmapper.WhitelistAffilGroupMapper',
                       'djangowind.auth.StaffMapper',
                       'djangowind.auth.SuperuserMapper']
AFFILS_WHITELIST = [
    'tlcxml.cunix.local:columbia.edu',
]

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
