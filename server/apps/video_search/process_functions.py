import requests

from apps.video_search.models import Videos


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

    return response_data


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


def get_new_youtube_videos(published_time):
    
    api_params = {
        'key': 'AIzaSyCBJ_jjCWHEIWJlAsN9LEfJgd2hUeUm_1k',
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

    return get_api_call(api_params)

def store_newly_published_videos(video_objects):

    Videos.objects.bulk_create(video_objects, batch_size=None)
    print('Data stored')
