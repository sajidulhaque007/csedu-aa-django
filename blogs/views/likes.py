from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from blogs.models import Blog, Like
from blogs.serializers import LikeManageSerializer

class LikeCreateDeleteView(generics.GenericAPIView):
    """
    API view for creating and deleting likes for a blog.
    """
    serializer_class = LikeManageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, blog_id):
        """
        Create a like for the given blog.
        """
        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=request.user, blog=blog)
        if created:
            return Response({"message": "Like created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "You have already liked this blog"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, blog_id):
        """
        Delete a like for the given blog.
        """
        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            like = Like.objects.get(user=request.user, blog=blog)
            like.delete()
            return Response({"message": "Like deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"error": "You have not liked this blog"}, status=status.HTTP_400_BAD_REQUEST)
