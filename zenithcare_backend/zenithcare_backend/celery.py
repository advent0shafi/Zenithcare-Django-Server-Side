# django_celery/celery.py
from __future__ import absolute_import, unicode_literals


import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zenithcare_backend.settings")
app = Celery("zenithcare_backend")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Add this line to set broker_connection_retry_on_startup to True
app.conf.enable_utc = False

app.conf.update(timezone = 'Europe/Paris')

app.autodiscover_tasks()