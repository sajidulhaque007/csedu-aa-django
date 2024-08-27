# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from django.db import models
# from django.utils import timezone
# from .managers import UserManager

# ROLE_CHOICES = [
#     ('admin', 'admin'),
#     ('regular', 'regular'),
# ]


# class User(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(unique=True, max_length=64)
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=64, null=True, blank=True)
#     last_name = models.CharField(max_length=64, null=True, blank=True)
#     role = models.CharField(max_length=25, choices=ROLE_CHOICES)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     date_joined = models.DateTimeField(default=timezone.now)

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']

#     objects = UserManager()

#     def __str__(self):
#         return self.username
