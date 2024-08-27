from django.db import models
from django.contrib.auth import get_user_model
from base.models import BaseModel
from . import Tag

User = get_user_model()

class Blog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    content = models.TextField()
    cover_picture = models.URLField(max_length=255, blank=True, null=True)  # Make cover_picture optional

    # Other fields or methods specific to your blog model

    class Meta:
        # Define any meta options for the blog model
        # For example, ordering, constraints, etc.
        pass
