import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iBlogger.settings')

from celery import Celery

app = Celery('iBlogger', include=['blog.tasks'])
app.config_from_object('iBlogger.celeryconfig')
