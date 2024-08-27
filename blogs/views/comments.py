from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from blogs.models import Comment
from blogs.serializers import CommentCreateUpdateSerializer

class CommentCreateUpdateView(generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    """
    API view for creating, updating, and deleting comments.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentCreateUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        # Set the user to the current authenticated user when creating a comment
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Only allow users to view comments they own
        return self.queryset.filter(user=self.request.user)
