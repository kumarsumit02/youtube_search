import requests

from django.utils import timezone

from apps.video_search.models import Videos, ApiKey


def get_existing_latest_video_published_time():

    try:
        latest_video = Videos.objects.values('published_at').latest('published_at')
        published_time = latest_video['published_at']
    except Videos.DoesNotExist:
        print('No video found')
        published_time = None

    return published_time


def get_api_response(api_params, page_token=None):

    url = 'https://www.googleapis.com/youtube/v3/search'

    if page_token:
        api_params.update({'pageToken': page_token})

    response = requests.request('GET', url, params=api_params)
    response_data = response.json()

    if response.status_code == 200:
        return response_data
    else:
        print('Error occured - ' + str(response_data))

    return {}


def get_api_call(api_params):

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
                logger.info('Skipping an item due to KeyError({})'.format(e))
                continue

        if 'nextPageToken' in response_data.keys():
            print('Getting data for nextPageToken - ', response_data['nextPageToken'])
            response_data = get_api_response(api_params, response_data['nextPageToken'])
        else:
            print('All data fetched count - ' + str(len(total_video_objects)))
            break
        
    return total_video_objects


def get_least_recently_used_api_key():

    return ApiKey.objects.order_by('last_used')[0]


def update_api_key(api_key_object):

    api_key_object.last_used = timezone.now()
    api_key_object.save()

def get_new_youtube_videos(published_time):
    
    api_key_object = get_least_recently_used_api_key()

    api_params = {
        'key': api_key_object.key,
        'type': 'video',
        'order': 'date',
        'part': 'snippet',
        'relevanceLanguage': 'en',
        'maxResults': 50,
        'q': 'stock market'
    }

    if published_time:
        formatted_published_time = published_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        api_params.update({'publishedAfter': formatted_published_time})

    new_video_objects = get_api_call(api_params)
    update_api_key(api_key_object)

    return new_video_objects


def store_newly_published_videos(video_objects):

    Videos.objects.bulk_create(video_objects, batch_size=None)
    print('Data stored')
