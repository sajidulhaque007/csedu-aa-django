from rest_framework import serializers
from blogs.models import Tag, Blog

class TagListSerializer(serializers.ModelSerializer):
    blogs_count = serializers.SerializerMethodField()  # Add a custom method for blogs count

    def get_blogs_count(self, obj):
        # Retrieve the count of blogs tagged with the current tag
        return Blog.objects.filter(tags=obj).count()

    class Meta:
        model = Tag
        fields = ('name', 'slug', 'blogs_count')
        read_only_fields = ('name', 'slug', 'blogs_count')
