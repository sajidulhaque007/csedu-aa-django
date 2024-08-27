from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from base.models import BaseModel
from users.managers import UserManager
import re
from django.core.exceptions import ValidationError
from users.models.choices import MEMBERSHIP_CHOICES, ROLE_CHOICES

class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email_address = models.EmailField(max_length=255, unique=True)
    referred_by = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=True)
    membership = models.CharField(max_length=16, choices=MEMBERSHIP_CHOICES, default='None')
    role = models.CharField(max_length=25, choices=ROLE_CHOICES, default='None')

    # Custom validator for the username field
    def validate_username(value):
        if len(value) < 3:
            raise ValidationError('Username must be at least 3 characters long.')
        if not re.match('^\w+$', value):
            raise ValidationError('Username can only contain letters, numbers, or underscores.')

    username = models.CharField(max_length=30, unique=True, validators=[validate_username])

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email_address'
    REQUIRED_FIELDS = ['email_address']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def is_staff(self):
        return self.is_admin
