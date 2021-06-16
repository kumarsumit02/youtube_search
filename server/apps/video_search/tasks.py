from celery.decorators import task

from .process_functions import (
    get_existing_latest_video_published_time,
    get_new_youtube_videos,
    store_newly_published_videos
)

@task(name="load_recently_published_videos")
def load_recently_published_videos():

    print('get_existing_latest_video_published_time')
    published_time = get_existing_latest_video_published_time()

    print('get_new_youtube_videos')
    video_objects = get_new_youtube_videos(published_time)

    print('store_newly_published_videos')
    store_newly_published_videos(video_objects)
