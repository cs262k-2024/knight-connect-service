import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField

from user.models import User

class Event(models.Model):
    id = models.UUIDField(
        primary_key=True, unique=True, blank=False, default=uuid.uuid4, editable=False
    )

    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    price = models.TextField(blank=True)

    location = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    cover_uri = models.TextField(blank=True)

    tags = ArrayField(
        models.CharField(max_length=100),
    )
