from django.db import models
from django.contrib.auth import get_user_model
from base.models import BaseModel
from . import Comment

User = get_user_model()

class CommentLike(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'comment')  # Ensure each user can like a comment only once

    def __str__(self):
        return f"{self.user.username} likes {self.comment.content}"
