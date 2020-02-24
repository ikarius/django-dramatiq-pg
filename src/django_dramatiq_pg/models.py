from enum import Enum

from django.contrib.postgres.fields import JSONField
from django.db import models


class State(Enum):
    QUEUED = 'queued'
    CONSUMED = 'consumed'
    REJECTED = 'rejected'
    DONE = 'done'


State.choices = tuple((state.name, state.value) for state in State)


class Task(models.Model):
    message_id = models.UUIDField(primary_key=True)
    queue_name = models.TextField(default='default')
    state = models.TextField(default=State.QUEUED, choices=State.choices)
    mtime = models.DateTimeField()  # Default = now()
    message = JSONField()
    result = JSONField()
    result_ttl = models.DateTimeField()

    class Meta:
        managed = False
        indexes = (
            models.Index(fields=['state', 'mtime']),
        )