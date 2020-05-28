#!/usr/bin/env python
import os
import sys
# https://pypi.org/project/python-dotenv/
import stripe
from dotenv import load_dotenv
load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY') # None
stripe.api_version = os.getenv('STRIPE_API_VERSION') # None

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pizza.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
