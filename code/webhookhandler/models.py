from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import jsonfield
import logging


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('webhookmodels.py')


class WebhookTransaction(models.Model):
    UNPROCESSED = 1
    PROCESSED = 2
    ERROR = 3

    STATUSES = (
        (UNPROCESSED, 'Unprocessed'),
        (PROCESSED, 'Processed'),
        (ERROR, 'Error'),
    )

    date_generated = models.DateTimeField()
    date_received = models.DateTimeField(default=timezone.now)
    body = jsonfield.JSONField(default={})
    request_meta = jsonfield.JSONField(default={})
    status = models.CharField(max_length=250, choices=STATUSES, default=UNPROCESSED)

    def __unicode__(self):
        return u'{0}'.format(self.date_event_generated)


