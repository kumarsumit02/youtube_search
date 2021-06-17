from rest_framework.viewsets import ModelViewSet

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.video_search.serializers import VideoSerializer, ApiKeySerializer
from apps.video_search.models import Videos, ApiKey


class VideoDataApi(ModelViewSet):
    """ ModelViewSet of Video APIs """

    http_method_names = ['get']
    serializer_class = VideoSerializer
    pagination_class = LimitOffsetPagination
    queryset = Videos.objects.all().order_by('-published_at')
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['title', 'description']


class ApiKeyDataApi(ModelViewSet):
    """ ModelViewSet of APIKeys APIs """

    http_method_names = ['get', 'post']
    queryset = ApiKey.objects.all()
    serializer_class = ApiKeySerializer
