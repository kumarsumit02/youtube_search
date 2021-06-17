from django.db.models import Q
from django_filters import FilterSet, CharFilter

from apps.video_search.models import Videos


class VideoFilter(FilterSet):

    title = CharFilter(field_name='title', method='filter_title')
    description = CharFilter(field_name='description', method='filter_description')

    def filter_title(self, queryset, name, value):
        """Filtering the Title """

        words = value.split(" ")

        # create a query to find the title which has searched words
        query = Q()
        for word in words:
            query = query & (Q(title__icontains=word))

        return queryset.filter(query)

    def filter_description(self, queryset, name, value):
        """Filtering the Description """

        words = value.split(" ")

        # create a query to find the title which has searched words
        query = Q()
        for word in words:
            query = query & (Q(description__icontains=word))

        return queryset.filter(query)

    class Meta:
        model = Videos
        fields = ['title', 'description', 'published_at', 'thumbnail_url']
        exclude = ['published_at', 'thumbnail_url', 'created_at', 'updated_at']
