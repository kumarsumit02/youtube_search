"""
    Storing all the Configurations at a single place.

        Ideally these should be in .env file :)
"""


class DjangoSettingsConfig(object):
    """Configirations related to Django Server"""

    API_RESPONSE_PAGE_SIZE = 30
    ENCRYPTION_KEY = "f164ec6bd6fbc4aef5647abc15199da0f9badcc1d2127bde2087ae0d794a9a0b"
    DJANGO_SECRET = 'ucuv6h6dlnl4xd2b*uxzwrt@z&47x_=2cdr$*340y8^&7)h-jx'


class BackgroundTaskConfig(object):
    """Configirations related to Background"""

    TIME_INTERVAL_SEC = 20
    API_URL = 'https://www.googleapis.com/youtube/v3/search'
    MAX_ROWS_IN_SINGLE_API_CALL = 60
    WORD_TO_QUERY = 'bitcoin'
    DEFAULT_API_KEY = 'AIzaSyAh6_Q2BGMTRoKnBqPPYqM-1FWiXVO3WYs'


class ModelConfig(object):
    """Configirations related to Database Models"""

    BULK_CREATE_BATCH_SIZE = 500
