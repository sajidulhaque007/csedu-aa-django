from django.db import models
from base.models import BaseModel


class Card(BaseModel):
    photo = models.URLField()
    title = models.CharField(max_length=255)
    caption = models.CharField(max_length=255)

    def __str__(self):
        return self.title