from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.models import SocialMediaLink, PresentAddress, Skill, AcademicHistory, WorkExperience
from users.serializers import SocialMediaLinkSerializer, PresentAddressSerializer, SkillSerializer, AcademicHistorySerializer, WorkExperienceSerializer

class SocialMediaLinkCreateView(generics.CreateAPIView):
    queryset = SocialMediaLink.objects.all()
    serializer_class = SocialMediaLinkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

class PresentAddressCreateView(generics.CreateAPIView):
    queryset = PresentAddress.objects.all()
    serializer_class = PresentAddressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

class SkillCreateView(generics.CreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

class WorkExperienceCreateView(generics.CreateAPIView):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        profile = self.request.user.profile
        serializer.save(profile=profile)

class AcademicHistoryCreateView(generics.CreateAPIView):
    queryset = AcademicHistory.objects.all()
    serializer_class = AcademicHistorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        profile = self.request.user.profile
        serializer.save(profile=profile)

class SocialMediaLinkListView(generics.ListAPIView):
    queryset = SocialMediaLink.objects.all()
    serializer_class = SocialMediaLinkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(profile=self.request.user.profile)

class SkillListView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(profile=self.request.user.profile)

class WorkExperienceListView(generics.ListAPIView):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(profile=self.request.user.profile)

class AcademicHistoryListView(generics.ListAPIView):
    queryset = AcademicHistory.objects.all()
    serializer_class = AcademicHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(profile=self.request.user.profile)
    
class PresentAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PresentAddress.objects.all()
    serializer_class = PresentAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(profile=self.request.user.profile)

class SocialMediaLinkDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SocialMediaLink.objects.all()
    serializer_class = SocialMediaLinkSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.profile.user != self.request.user:
            self.permission_denied(self.request)
        return obj

class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.profile.user != self.request.user:
            self.permission_denied(self.request)
        return obj

class WorkExperienceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.profile.user != self.request.user:
            self.permission_denied(self.request)
        return obj

class AcademicHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AcademicHistory.objects.all()
    serializer_class = AcademicHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.profile.user != self.request.user:
            self.permission_denied(self.request)
        return obj