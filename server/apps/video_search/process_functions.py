import logging

import requests

from django.utils import timezone

from apps.video_search.models import Videos, ApiKey
from youtube_project.config import BackgroundTaskConfig

logger = logging.getLogger('application')


def get_api_response(api_params, page_token=None):
    """ Does the GET call to youtube API"""

    url = BackgroundTaskConfig.API_URL

    if page_token:
        api_params.update({'pageToken': page_token})

    response = requests.request('GET', url, params=api_params)
    response_data = response.json()

    if response.status_code != 200:
        logger.error(f'Occured while getting data from youtube  -  {str(response_data)}')

    return response_data


def get_new_video_objects(api_params):
    """ Returns the list of new video objects"""

    total_video_objects = []
    response_data = get_api_response(api_params)

    while True:
        for item in response_data.get('items', []):
            try:
                snippet = item['snippet']

                video_data_dict = {
                    'title': snippet['title'],
                    'description': snippet['description'],
                    'published_at': snippet['publishedAt'],
                    'thumbnail_url': snippet['thumbnails']['default']['url'],
                }

                video_object = Videos(**video_data_dict)
                total_video_objects.append(video_object)

            except KeyError as e:
                logger.info(f'Skipping an item due to KeyError({e})')
                continue

        # get data until last page
        if 'nextPageToken' in response_data.keys():
            response_data = get_api_response(api_params, response_data['nextPageToken'])
        else:
            logger.info(f'All data fetched count - {str(len(total_video_objects))}')
            break

    return total_video_objects


def update_api_key(api_key_object):
    """ Updates the last used time of API Key """

    api_key_object.last_used = timezone.now()
    api_key_object.save()


def get_new_youtube_videos(published_time, api_key_object):
    """ Returns the list of new youtube video objects """

    if api_key_object:
        api_key = api_key_object.key
    else:
        api_key = BackgroundTaskConfig.DEFAULT_API_KEY

    api_params = {
        'key': api_key,
        'type': 'video',
        'order': 'date',
        'part': 'snippet',
        'relevanceLanguage': 'en',
        'maxResults': BackgroundTaskConfig.MAX_ROWS_IN_SINGLE_API_CALL,
        'q': BackgroundTaskConfig.WORD_TO_QUERY
    }

    # Fetch only those videos whose published time is greater than that of already existing videos
    if published_time:
        formatted_published_time = published_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        api_params.update({'publishedAfter': formatted_published_time})

    new_video_objects = get_new_video_objects(api_params)

    # if key is picked from table, update last used timing
    if api_key_object:
        update_api_key(api_key_object)

    return new_video_objects
