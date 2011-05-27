import os
import sys
path = '/local/infoini_dg/infoini'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'infoini.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
