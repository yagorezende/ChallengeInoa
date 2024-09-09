from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'challenge_inoa.settings')

app = Celery('challenge_inoa')

# Load django settings for Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks in Django applications
app.autodiscover_tasks()
