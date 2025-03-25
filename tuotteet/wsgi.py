"""
WSGI config for tuotteet project.

This file exposes the WSGI callable as a module-level variable named `application`.
See https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/ for details.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tuotteet.settings')

application = get_wsgi_application()
