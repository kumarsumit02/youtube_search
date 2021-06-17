from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from datetime import timedelta

from youtube_project.config import BackgroundTaskConfig

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_project.settings')

app = Celery('youtube_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# Configurations of job timings
app.conf.beat_schedule = {
    'youtube_videos_dataload': {
        'task': 'load_recently_published_videos',
        'schedule': timedelta(seconds=BackgroundTaskConfig.TIME_INTERVAL_SEC),
    }
}
