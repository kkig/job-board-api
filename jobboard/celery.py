import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobboard.settings')

app = Celery('jobboard')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in all registered Django app configs
app.autodiscover_tasks()

# import jobs.tasks # force import so Celery sess the task

# Starting Celery
if __name__ == '__main__':
    app.start()
