from rest_framework import serializers
from .models import Videos, ApiKey


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        """Meta class to map serializer's fields with the model fields."""

        model = Videos
        exclude = []
        read_only_fields = ('title', 'description', 'published_at', 'thumbnail_url')


class ApiKeySerializer(serializers.ModelSerializer):

    class Meta:
        """Meta class to map serializer's fields with the model fields."""

        model = ApiKey
        fields = ('key', 'last_used')
