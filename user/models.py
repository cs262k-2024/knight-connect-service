import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField

class User(models.Model):
    id = models.UUIDField(
        primary_key=True, unique=True, blank=False, default=uuid.uuid4, editable=False
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    preferences = ArrayField(
        models.CharField(max_length=100),
    )

    password = models.CharField(max_length=255)
    bio = models.TextField()

    joined_events = models.ManyToManyField('event.Event', related_name='participants', blank=True)

    friends = models.ManyToManyField('User', blank=True, related_name='friends+')
    incoming_requests = models.ManyToManyField('User', blank=True, related_name='incoming_requests+')
