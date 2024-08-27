from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from blogs.models import Blog
from blogs.serializers import BlogCreateUpdateSerializer, BlogReadSerializer
from rest_framework.exceptions import PermissionDenied

class BlogUpdateRetrieveDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BlogReadSerializer
        return BlogCreateUpdateSerializer

    def perform_update(self, serializer):
        # Set the user of the blog to the currently logged in user during update
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        # Pass the context to the serializer
        context = super().get_serializer_context()
        context['blog'] = self.get_object()
        return context

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        obj = generics.get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        # Use partial=True for PATCH requests
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        tags_data = request.data.get('tags',[])  # Remove tags from request data
        # Update tags if provided
        if tags_data is not None:
            serializer._get_or_create_tags(tags_data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        # Delegate to the update method for PATCH requests
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Override destroy method to check if the request user is the owner of the blog
        instance = self.get_object()
        if instance.user != request.user and not request.user.is_superuser:
            raise PermissionDenied("You can only delete your own blog except when you're a superuser.")
        return super().destroy(request, *args, **kwargs)

class BlogCreateView(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Set the user of the blog to the currently logged in user during creation
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        tags_data = request.data.get('tags', []) # Remove tags from request data
        serializer = self.get_serializer(data=request.data)
        # Update tags
        if tags_data:
            serializer._get_or_create_tags(tags_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)



        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
