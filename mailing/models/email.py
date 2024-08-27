from django.db import models
from users.models import User
from django.core.validators import validate_email

class CommonEmailAddress(models.Model):
    email = models.EmailField(unique=True, validators=[validate_email])

    def __str__(self):
        return self.email

    def has_user(self):
        """
        Returns True if a user exists with this email address, False otherwise.
        """
        return User.objects.filter(email_address=self.email).exists()

    def get_user(self):
        """
        Returns the User instance with this email address, or None if no such user exists.
        """
        try:
            return User.objects.get(email_address=self.email)
        except User.DoesNotExist:
            return None