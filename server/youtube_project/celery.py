from __future__ import absolute_import, unicode_literals
# from __future__ import absolute_import
import os
from celery import Celery
# from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_project.settings')

app = Celery('youtube_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

app.conf.beat_schedule = {
    'add-every-60-seconds': {
        'task': 'load_recently_published_videos',
        'schedule': 60.0,
    }
}