from django.db.models import Count
from rest_framework import generics, permissions
from blogs.models import Tag
from blogs.serializers import TagListSerializer

class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.annotate(blogs_count=Count('blog')).order_by('-blogs_count')
    serializer_class = TagListSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require authentication to access the view
