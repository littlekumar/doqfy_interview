from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Snippet(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    secret_key = models.CharField(max_length=255, blank=True, null=True)
    shareable_url = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.text