from django.db import models
from django.contrib.auth import get_user_model
from base.models import BaseModel
from . import Blog

User = get_user_model()

class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()

    class Meta:
        # Define any meta options for the comment model
        # For example, ordering, constraints, etc.
        pass
