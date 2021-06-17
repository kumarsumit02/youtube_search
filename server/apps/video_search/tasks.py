import logging

from celery.decorators import task

from apps.video_search.models import Videos, ApiKey
from apps.video_search.process_functions import get_new_youtube_videos

logger = logging.getLogger('application')


@task(name="load_recently_published_videos")
def load_recently_published_videos():
    """ Loads the newly published videos to the database """

    logger.info("Getting Latest Published Video Time from Table")
    published_time = Videos.get_latest_published_time()

    logger.info("Getting Least Recently Used API Key from Table")
    api_key_object = ApiKey.get_lru_api_key_object()

    logger.info("Getting Data from YouTube API")
    new_video_objects = get_new_youtube_videos(published_time, api_key_object)

    logger.info("Saving New Videos Data to Table")
    Videos.bulk_create_videos(new_video_objects)
