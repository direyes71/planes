import os, sys
apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)
sys.path.append('/var/django/aplicacion')
os.environ['DJANGO_SETTINGS_MODULE'] = 'aplicacion.settings'
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
