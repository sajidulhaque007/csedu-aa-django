from rest_framework import serializers
from blogs.models import CommentLike

class CommentLikeManageSerializer(serializers.ModelSerializer):
    """
    Serializer for managing comment likes.
    """
    class Meta:
        model = CommentLike
        fields = '__all__'