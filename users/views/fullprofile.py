from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import Profile
from users.serializers import FullProfileSerializer
from users.models import User
from django.http import Http404
from rest_framework import generics, permissions

class FullProfileDetail(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = FullProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            user = User.objects.get(username=self.kwargs['username'])
        except User.DoesNotExist:
            raise Http404
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            raise Http404
        return profile

class OwnFullProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = FullProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = FullProfileSerializer(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = FullProfileSerializer(instance = profile, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

