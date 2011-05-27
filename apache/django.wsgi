import os
import sys
sys.path.append('/local/infoini_dg')
sys.path.append('/local/infoini_dg/infoini')

os.environ['DJANGO_SETTINGS_MODULE'] = 'infoini.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
