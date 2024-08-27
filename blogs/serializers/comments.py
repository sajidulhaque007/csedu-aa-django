from rest_framework import serializers
from blogs.models import Comment

class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating comments.
    """

    class Meta:
        model = Comment
        fields = ('blog', 'content')
        read_only_fields = ('user',)

    def create(self, validated_data):
        # Set the user to the current authenticated user
        user = self.context['request'].user
        validated_data['user'] = user

        # Create and return the comment
        comment = Comment(**validated_data)
        comment.save()
        return comment

    def update(self, instance, validated_data):
        # Check if the user is the same as the comment's user
        user = self.context['request'].user
        if instance.user != user:
            raise serializers.ValidationError('You do not have permission to update this comment.')

        # Update the content field of the comment
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
