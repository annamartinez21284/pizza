"""
WSGI config for pizza project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
# https://pypi.org/project/python-dotenv/
import stripe
from dotenv import load_dotenv
load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY') # None
stripe.api_version = os.getenv('STRIPE_API_VERSION') # None

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pizza.settings")

application = get_wsgi_application()
