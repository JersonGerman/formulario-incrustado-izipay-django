import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_formulario_incrustado.settings')

application = get_wsgi_application()
