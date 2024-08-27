from rest_framework import serializers, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from blogs.models import Comment, CommentLike
from blogs.serializers import CommentLikeManageSerializer

class CommentLikeCreateDeleteView(generics.GenericAPIView):
    """
    API view for creating and deleting comment likes.
    """
    serializer_class = CommentLikeManageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        """
        Create a like for the given comment.
        """
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
        if created:
            return Response({"message": "Comment like created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "You have already liked this comment"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        """
        Delete a like for the given comment.
        """
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            like = CommentLike.objects.get(user=request.user, comment=comment)
            like.delete()
            return Response({"message": "Comment like deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except CommentLike.DoesNotExist:
            return Response({"error": "You have not liked this comment"}, status=status.HTTP_400_BAD_REQUEST)
