from rest_framework import serializers
from blogs.models import Like

class LikeManageSerializer(serializers.ModelSerializer):
    """
    Serializer for managing likes.
    """
    class Meta:
        model = Like
        fields = '__all__'
