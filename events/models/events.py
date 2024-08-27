from django.db import models
from base.models import BaseModel
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings

class EventManager(models.Manager):    
    def create(self, title, description, location, start_datetime=None, end_datetime=None, cover_picture=None, creator=None):
        if not creator.is_admin:
            raise ValueError('Only admin users can create events')

        event = Event(
            creator=creator,
            title=title,
            description=description,
            location=location,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            cover_picture=cover_picture,
        )

        event.save()
        event.managers.add(creator) 
        return event

class Event(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    cover_picture = models.URLField(blank=True, null=True)
    managers = models.ManyToManyField('users.User', related_name='managed_events')
    guests = models.ManyToManyField('users.User', related_name='attending_events')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, editable=False, related_name='created_events')

    objects = EventManager()

    def clean(self):
        """
        Validates that the start_datetime is in the present or future and that the end_datetime is after the start_datetime.
        """
        if self.start_datetime < timezone.now():
            raise ValidationError('Start datetime must be in the present or future.')
        if self.end_datetime <= self.start_datetime:
            raise ValidationError('End datetime must be after start datetime.')
        
    def __str__(self):
        return self.title
