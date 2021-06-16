from rest_framework import serializers
from .models import Videos


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        """Meta class to map serializer's fields with the model fields."""

        model = Videos
        exclude = []
        read_only_fields = ('title', 'description', 'published_at', 'thumbnail_url')
