from django.http import Http404
from rest_framework import generics, permissions
from users.models import SocialMediaLink, PresentAddress, Skill, AcademicHistory, WorkExperience, User
from users.serializers import SocialMediaLinkSerializer, PresentAddressSerializer, SkillSerializer, AcademicHistorySerializer, WorkExperienceSerializer

class SocialMediaLinkUserListView(generics.ListAPIView):
    serializer_class = SocialMediaLinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            user = User.objects.get(username=self.kwargs['username'])
        except User.DoesNotExist:
            raise Http404

        # Filter the queryset based on the retrieved user's profile object
        return SocialMediaLink.objects.filter(profile=user.profile)

class SkillUserListView(generics.ListAPIView):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            user = User.objects.get(username=self.kwargs['username'])
        except User.DoesNotExist:
            raise Http404

        # Filter the queryset based on the retrieved user's profile object
        return Skill.objects.filter(profile=user.profile)

class WorkExperienceUserListView(generics.ListAPIView):
    serializer_class = WorkExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            user = User.objects.get(username=self.kwargs['username'])
        except User.DoesNotExist:
            raise Http404

        # Filter the queryset based on the retrieved user's profile object
        return WorkExperience.objects.filter(profile=user.profile)

class AcademicHistoryUserListView(generics.ListAPIView):
    serializer_class = AcademicHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            user = User.objects.get(username=self.kwargs['username'])
        except User.DoesNotExist:
            raise Http404

        # Filter the queryset based on the retrieved user's profile object
        return AcademicHistory.objects.filter(profile=user.profile)

class PresentAddressUserDetailView(generics.RetrieveAPIView):
    serializer_class = PresentAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            user = User.objects.get(username=self.kwargs['username'])
        except User.DoesNotExist:
            raise Http404

        # Get the object based on the provided username
        try:
            obj = user.profile.present_address
        except PresentAddress.DoesNotExist:
            raise Http404

        self.check_object_permissions(self.request, obj)

        return obj