"""
WSGI config for web_piket project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_piket.settings')

application = get_wsgi_application()
