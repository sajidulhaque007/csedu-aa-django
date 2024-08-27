from rest_framework import serializers
from users.models import Profile, WorkExperience, Skill, SocialMediaLink, AcademicHistory, PresentAddress

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'profile_picture', 'date_of_birth', 'sex', 'batch_number', 'registration_number', 'hometown', 'phone_number']
        read_only_fields = ['id']
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.user != user:
            raise serializers.ValidationError('Cannot update profile of another user')
        return super().update(instance, validated_data)

class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = ('id', 'profile', 'platform_name', 'link')
        read_only_fields = ('id', 'profile')

    def validate(self, data):
        if self.instance and self.instance.profile.user != self.context['request'].user:
            raise serializers.ValidationError('You can only update your own social media links.')
        return data

class PresentAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresentAddress
        fields = ('id', 'city', 'country', 'profile')
        read_only_fields = ('id', 'profile')

    def validate(self, data):
        if self.instance and self.instance.profile.user != self.context['request'].user:
            raise serializers.ValidationError('You can only update your own present address.')
        return data

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name', 'proficiency', 'description', 'profile')
        read_only_fields = ('id', 'profile')

    def validate(self, data):
        if self.instance and self.instance.profile.user != self.context['request'].user:
            raise serializers.ValidationError('You can only update your own skills.')
        return data

class AcademicHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicHistory
        fields = ('id', 'profile', 'institution_name', 'degree_name', 'concentration', 'start_date', 'graduation_date', 'is_currently_studying', 'result')
        read_only_fields = ('id', 'profile')
    
    def to_internal_value(self, data):
        if data.get('start_date') == '':
            data['start_date'] = None
        if data.get('graduation_date') == '':
            data['graduation_date'] = None
        return super().to_internal_value(data)

    def validate(self, data):
        if self.instance and self.instance.profile.user != self.context['request'].user:
            raise serializers.ValidationError('You can only update your own academic histories.')
        return data


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ('id', 'profile', 'company_name', 'branch', 'position', 'starting_date', 'ending_date', 'currently_working', 'description')
        read_only_fields = ('id', 'profile')
    
    def to_internal_value(self, data):
        if data.get('starting_date') == '':
            data['starting_date'] = None
        if data.get('ending_date') == '':
            data['ending_date'] = None
        return super().to_internal_value(data)

    def validate(self, data):
        if self.instance and self.instance.profile.user != self.context['request'].user:
            raise serializers.ValidationError('You can only update your own work experiences.')
        return data
    
class FullProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email_address = serializers.EmailField(source='user.email_address', read_only=True)
    is_admin = serializers.BooleanField(source='user.is_admin', read_only=True)
    is_superuser = serializers.BooleanField(source='user.is_superuser' , read_only= True)
    social_media_links = SocialMediaLinkSerializer(many=True, required=False)
    present_address = PresentAddressSerializer(required=False)
    skills = SkillSerializer(many=True, required=False)
    academic_histories = AcademicHistorySerializer(many=True, required=False)
    work_experiences = WorkExperienceSerializer(many=True, required=False)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'email_address', 'first_name', 'last_name', 'profile_picture', 'is_admin','is_superuser','date_of_birth', 'sex', 'batch_number', 'registration_number', 'hometown', 'phone_number', 'social_media_links', 'present_address', 'skills', 'academic_histories', 'work_experiences']
        read_only_fields = ['id', 'username', 'email']

    def to_internal_value(self, data):
        if data.get('date_of_birth') == '':
            data['date_of_birth'] = None
        return super().to_internal_value(data)
    
    def to_representation(self, instance):
        user = self.context.get('request').user
        data = super().to_representation(instance)
        if instance.user != user:
            data.pop('is_superuser')
        return data
    
    def update(self, instance, validated_data):
        if self.partial:
            return self.partial_update(instance, validated_data)
        
        user = self.context['request'].user
        if instance.user != user:
            raise serializers.ValidationError('Cannot update profile of another user')
        
        social_media_links_data = validated_data.pop('social_media_links', [])
        present_address_data = validated_data.pop('present_address', {})
        skills_data = validated_data.pop('skills', [])
        academic_histories_data = validated_data.pop('academic_histories', [])
        work_experiences_data = validated_data.pop('work_experiences', [])
        
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        instance.social_media_links.all().delete()
        for link_data in social_media_links_data:
            SocialMediaLink.objects.create(profile=instance, **link_data)

        try:
            instance.present_address.delete()
        except:
            pass
        PresentAddress.objects.create(profile=instance, **present_address_data)
    
        instance.skills.all().delete()
        for skill_data in skills_data:
            Skill.objects.create(profile=instance, **skill_data)
    
        instance.academic_histories.all().delete()
        for academic_history_data in academic_histories_data:
            AcademicHistory.objects.create(profile=instance, **academic_history_data)
    
        instance.work_experiences.all().delete()
        for work_experience_data in work_experiences_data:
            WorkExperience.objects.create(profile=instance, **work_experience_data)
        
        instance.save()
        
        return instance
    
    def partial_update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.user != user:
            raise serializers.ValidationError('Cannot update profile of another user')
        
        social_media_links_data = validated_data.pop('social_media_links', None)
        present_address_data = validated_data.pop('present_address', None)
        skills_data = validated_data.pop('skills', None)
        academic_histories_data = validated_data.pop('academic_histories', None)
        work_experiences_data = validated_data.pop('work_experiences', None)
        
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        if social_media_links_data is not None:
            instance.social_media_links.all().delete()
            for link_data in social_media_links_data:
                SocialMediaLink.objects.create(profile=instance, **link_data)

        if present_address_data is not None:
            try:
                instance.present_address.delete()
            except:
                pass
            PresentAddress.objects.create(profile=instance, **present_address_data)
        
        if skills_data is not None:
            instance.skills.all().delete()
            for skill_data in skills_data:
                Skill.objects.create(profile=instance, **skill_data)
        
        if academic_histories_data is not None:
            instance.academic_histories.all().delete()
            for academic_history_data in academic_histories_data:
                AcademicHistory.objects.create(profile=instance, **academic_history_data)
        
        if work_experiences_data is not None:
            instance.work_experiences.all().delete()
            for work_experience_data in work_experiences_data:
                WorkExperience.objects.create(profile=instance, **work_experience_data)
        
        instance.save()
        
        return instance