from django.db import models
import pgcrypto


class Videos(models.Model):
    title = models.CharField(max_length=500, blank=False)
    description = models.TextField(blank=True)
    published_at = models.DateTimeField(blank=False, db_index=True)
    thumbnail_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        """String representation of the model."""
        return self.title

    class Meta:
        get_latest_by = 'published_at'


class ApiKey(models.Model):
    key =  pgcrypto.EncryptedTextField(unique=True)
    last_used = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the model."""
        return self.key