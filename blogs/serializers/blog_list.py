from rest_framework import serializers
from bs4 import BeautifulSoup
from blogs.models import Blog
from .blog_read import TagSerializer

class BlogListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    content_head = serializers.SerializerMethodField(read_only = True)
    tags = TagSerializer(many=True)
    can_delete = serializers.SerializerMethodField(read_only = True) 

    class Meta:
        model = Blog
        fields = ('id', 'user', 'title', 'tags', 'content_head', 'created_at', 'updated_at', 'cover_picture', 'can_delete')

    def get_user(self, obj):
        # Return a serialized representation of the user (username, first_name, last_name)
        user = obj.user
        return {
            'username': user.username,
            'first_name': user.profile.first_name,
            'last_name': user.profile.last_name
        }
    
    def get_can_delete(self, obj):
        # Check if the current user can delete the blog
        user = self.context['request'].user
        if user != obj.user and not user.is_superuser :
            return False  
        return True

    def get_content_head(self, obj):
        # Extract text from HTML content and generate a summary
        content = obj.content
        soup = BeautifulSoup(content, 'html.parser')  # Parse HTML content
        text = soup.get_text()  # Extract text from HTML
        words = text.split()  # Split the text by space
        summary = ' '.join(words[:10])  # Extract the first 10 words as the summary

        # Add "..." at the end of the summary if there is more content remaining in the text
        if len(words) > 10:
            summary += "..."
            
        return summary
