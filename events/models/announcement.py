from django.db import models
from base.models import BaseModel
from django.core.exceptions import ValidationError
from django.conf import settings
from events.models import Event

class EventAnnouncement(BaseModel):
    text = models.TextField()
    picture = models.URLField(blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='announcements')
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_announcements')

    def clean(self):
        """
        Validates that the user who posted the announcement is a manager of the associated event.
        """
        if self.posted_by not in self.event.managers.all():
            raise ValidationError('Only managers of the associated event can post announcements.')
