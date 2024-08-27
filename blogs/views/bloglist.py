from django.db.models import Count, F
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from blogs.models import Blog
from blogs.serializers import BlogListSerializer
from django.db.models import Q

class BlogListAPIView(generics.ListAPIView):
    serializer_class = BlogListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        # Pass the context to the serializer
        context = super().get_serializer_context()
        return context

    def get_queryset(self):
        queryset = Blog.objects.all()
        tag_slugs = self.request.query_params.getlist('tags__slug', [])
        if tag_slugs:
            queryset = queryset.annotate(tag_count=Count('tags__slug', filter=Q(tags__slug__in=tag_slugs)))
            queryset = queryset.filter(tag_count__gte=1)
            queryset = queryset.order_by('-tag_count', '-updated_at')
        else:
            queryset = queryset.order_by('-updated_at')

        page_size = self.request.query_params.get('page_size', None)

        if page_size:
            self.pagination_class = PageNumberPagination
            self.pagination_class.page_size = int(page_size)
        else:
            self.pagination_class = None

        return queryset


class UserBlogListAPIView(generics.ListAPIView):
    serializer_class = BlogListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the username from the URL parameters
        username = self.kwargs['username']

        # Filter blogs by the username
        queryset = Blog.objects.filter(user__username=username)

        return queryset

class SelfBlogListAPIView(generics.ListAPIView):
    serializer_class = BlogListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter blogs by the currently authenticated user
        user = self.request.user
        queryset = Blog.objects.filter(user=user)

        return queryset
