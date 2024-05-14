"""
ASGI config for orders project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import sys

from django.core.asgi import get_asgi_application

path = "C:/Users/tkaac/PycharmProjects/diplom/orders"
if path not in sys.path:
    sys.path.insert(0, path)

os.environ["DJANGO_SETTINGS_MODULE"] = "orders.settings"

application = get_asgi_application()
