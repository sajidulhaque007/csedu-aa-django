from rest_framework import serializers
from blogs.models import Blog, Tag

class BlogCreateUpdateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Blog
        fields = ('id', 'user', 'title', 'content', 'cover_picture', 'tags', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_user(self, value):
        """
        Validate that the user making the request is the same as the blog owner.
        """
        blog = self.context.get('blog')
        request_user = self.context['request'].user
        if blog and blog.user != request_user:
            raise serializers.ValidationError("You can only update your own blog.")
        return value

    def update(self, instance, validated_data):
        """
        Perform full update or partial update on the blog instance
        depending on the request method.
        """
        request = self.context['request']
        tags_data = validated_data.pop('tags', None)
        if request.method == 'PATCH':
            # Perform partial update for PATCH request
            instance.title = validated_data.get('title', instance.title)
            instance.content = validated_data.get('content', instance.content)
            instance.cover_picture = validated_data.get('cover_picture', instance.cover_picture)
            # Update tags
            if tags_data is not None:
                instance.tags.set(tags_data)
            
            else :
                tags = instance.tags.all()
                instance.tags.set(tags)

        else:
            # Perform full update for PUT request
            instance.title = validated_data['title']
            instance.content = validated_data['content']
            instance.cover_picture = validated_data['cover_picture']
            # Update tags
            if tags_data is not None:
                instance.tags.set(tags_data)
            
            else :
                tags = []
                instance.tags.set(tags)

        instance.save()

        return instance

    def _get_or_create_tags(self, tags_data):
        """
        Get or create Tag instances from the provided tags_data list.
        """
        tags = []
        for tag_slug in tags_data:
            try:
                tag = Tag.objects.get(slug=tag_slug)
            except Tag.DoesNotExist:
                tag = Tag.objects.create(slug=tag_slug)
            tags.append(tag)
        return tags
