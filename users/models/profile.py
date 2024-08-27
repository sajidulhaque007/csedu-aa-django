from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_picture = models.URLField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    batch_number = models.CharField(max_length=10)
    registration_number = models.CharField(max_length=20, null=True, blank=True)
    hometown = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class SocialMediaLink(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='social_media_links')
    platform_name = models.CharField(max_length=50)
    link = models.URLField()

    def __str__(self):
        return f"{self.profile.user.username}'s {self.platform_name} link"

class PresentAddress(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='present_address')

    def __str__(self):
        return f"{self.city}, {self.country}"

class Skill(models.Model):
    PROFICIENCY_CHOICES = (
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert'),
    )

    name = models.CharField(max_length=255)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES)
    description = models.CharField(max_length=255, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')

    def __str__(self):
        return f"{self.name} ({self.proficiency})"

class AcademicHistory(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='academic_histories')
    institution_name = models.CharField(max_length=255)
    degree_name = models.CharField(max_length=255)
    concentration = models.CharField(max_length=255)
    start_date = models.DateField()
    graduation_date = models.DateField(null=True, blank=True)
    is_currently_studying = models.BooleanField(default=False)
    result = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.degree_name} ({self.concentration}) at {self.institution_name}"


class WorkExperience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='work_experiences')
    company_name = models.CharField(max_length=255)
    branch = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255)
    starting_date = models.DateField()
    ending_date = models.DateField(null=True, blank=True)
    currently_working = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-ending_date', '-starting_date']

    def __str__(self):
        return f"{self.position} at {self.company_name}"

    def save(self, *args, **kwargs):
        if not self.currently_working and not self.ending_date:
            raise ValueError('Ending date is required if not currently working')
        if self.currently_working and self.ending_date:
            raise ValueError('Ending date should be empty if currently working')
        if self.ending_date and self.starting_date > self.ending_date:
            raise ValueError('Starting date should be before ending date')
        super().save(*args, **kwargs)

    def is_currently_working(self):
        if self.currently_working:
            return True
        if not self.ending_date:
            return False
        return self.ending_date > timezone.now().date()

    def duration(self):
        if not self.ending_date:
            return None
        return self.ending_date - self.starting_date
