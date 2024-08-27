from django.db import models
from django.contrib.auth import get_user_model
from base.models import BaseModel
from . import Blog 

User = get_user_model()

class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    
    
    class Meta:
        # Use unique_together to enforce unique constraint on the combination
        # of user and blog fields, ensuring that a user can like a blog only once
        unique_together = ('user', 'blog')
