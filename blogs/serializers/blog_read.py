from rest_framework import serializers
from blogs.models import Blog, Comment, Like, Tag

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        # Retrieve the user profile information for the like's user
        user = obj.user
        profile = user.profile
        return {
            'username': user.username,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'profile_picture': profile.profile_picture  # Use profile_picture directly
        }

    class Meta:
        model = Like
        fields = ('id', 'user', 'created_at', 'updated_at')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    def get_user(self, obj):
        # Retrieve the user profile information for the comment's user
        user = obj.user
        profile = user.profile
        return {
            'username': user.username,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'profile_picture': profile.profile_picture  # Use profile_picture directly
        }

    def get_likes_count(self, obj):
        # Retrieve the count of likes on the comment
        return obj.likes.count()

    def get_is_liked(self, obj):
        # Retrieve the current user from the request context
        user = self.context['request'].user

        # Check if the current user has liked the comment
        return obj.likes.filter(user=user).exists()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'likes_count', 'is_liked', 'created_at', 'updated_at')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('slug',)  # Use the 'slug' field to serialize tags

class BlogReadSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True)
    user = serializers.SerializerMethodField(read_only = True)
    likes_count = serializers.SerializerMethodField(read_only = True)
    comments_count = serializers.SerializerMethodField(read_only = True)  
    is_liked = serializers.SerializerMethodField(read_only = True) 
    can_delete = serializers.SerializerMethodField(read_only = True) 

    def get_user(self, obj):
        # Retrieve the user profile information for the blog's user
        user = obj.user
        profile = user.profile
        return {
            'username': user.username,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'profile_picture': profile.profile_picture
        }

    def get_likes_count(self, obj):
        # Retrieve the number of likes associated with the blog
        return obj.likes.count()

    def get_comments_count(self, obj):
        # Retrieve the number of comments associated with the blog
        return obj.comments.count()  # Assuming comments is a related name for comments in the Blog model

    def get_is_liked(self, obj):
        # Check if the current user has liked the blog
        user = self.context['request'].user
        if user.is_authenticated:
            # If user is authenticated, check if the user has liked the blog
            return obj.likes.filter(user=user).exists()
        return False  # If user is not authenticated, return False for is_liked field
    
    def get_can_delete(self, obj):
        # Check if the current user can delete the blog
        user = self.context['request'].user
        if user != obj.user and not user.is_superuser :
            return False  
        return True
    
    class Meta:
        model = Blog
        fields = ('id', 'user', 'title', 'tags', 'content', 'comments', 'likes', 'likes_count', 'comments_count', 'created_at', 'updated_at', 'cover_picture', 'is_liked', 'can_delete') 
        read_only_fields = ('id', 'user', 'comments', 'likes', 'likes_count', 'comments_count', 'created_at', 'updated_at')
