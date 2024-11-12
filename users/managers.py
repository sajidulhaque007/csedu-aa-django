from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email_address, password=None, referred_by=None, is_admin=False, is_superuser=False, is_pending=True):
        if not username:
            raise ValueError("Users must have a username")
        if not email_address:
            raise ValueError("Users must have an email address")
        user = self.model(
            username=username,
            email_address=self.normalize_email(email_address),
            referred_by=referred_by,
            is_admin=is_admin,
            is_superuser=is_superuser,
            is_pending=is_pending,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email_address, password, referred_by=None):
        user = self.create_user(
            username=username,
            email_address=self.normalize_email(email_address),
            password=password,
            # role=role,
            referred_by=referred_by,
            is_admin=True,
            is_superuser=True,
            is_pending=False,
        )
        return user
    
    def change_password(self, user, old_password, new_password):
        # Check if the old password matches the user's current password
        if not user.check_password(old_password):
            raise ValueError("Old password is incorrect")

        # Check if the new password is the same as the old password
        if old_password == new_password:
            raise ValueError("New password cannot be the same as the old password")

        # Set the new password and save the user
        user.set_password(new_password)
        user.save()
        return user

    def reset_password(self, user, new_password):
        # Check if the new password is the same as the old password
        if user.check_password(new_password):
            raise ValueError("New password cannot be the same as the old password")

        # Set the new password and save the user
        user.set_password(new_password)
        user.save()
        return user

    def make_user_admin(self, user):
        user.is_admin = True
        user.save()
        return user

    def remove_user_adminship(self, user):
        """
        Remove adminship from a user.
        Superusers cannot have their adminship removed.
        """
        if user.is_superuser:
            raise ValueError("Cannot remove adminship from a superuser")
        
        user.is_admin = False
        user.save()
        return user

    def accept_pending(self, user):
        user.is_pending = False
        user.save()
        return user
    
    def changeMembership(self, user, membership_choice):
        user.membership = membership_choice
        user.save()
        return user
    