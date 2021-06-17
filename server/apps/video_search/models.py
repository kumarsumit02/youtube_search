from django.db import models
from encrypted_fields import fields

from youtube_project.config import ModelConfig

class Videos(models.Model):
    """ Model to Store Video details """

    title = models.CharField(max_length=500, blank=False)
    description = models.TextField(blank=True)
    published_at = models.DateTimeField(blank=False, db_index=True)
    thumbnail_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the model """
        return self.title

    def get_latest_published_time():
        """returns the last published video from the table"""
        if Videos.objects.exists():
            return Videos.objects.values('published_at').order_by('-published_at')[0]['published_at']
        else:
            return None

    def bulk_create_videos(video_objects):
        """ creates multiple video entries """
        Videos.objects.bulk_create(video_objects, batch_size=ModelConfig.BULK_CREATE_BATCH_SIZE)


class ApiKey(models.Model):
    """ Model to store API Keys """

    key =  fields.EncryptedCharField(max_length=255)
    last_used = models.DateTimeField(null=True)

    def __str__(self):
        """String representation of the model """
        return self.key

    def get_lru_api_key_object():
        """ returns least recently used API key"""
        if ApiKey.objects.exists():
            return ApiKey.objects.order_by('last_used')[0]
        else:
            return None
