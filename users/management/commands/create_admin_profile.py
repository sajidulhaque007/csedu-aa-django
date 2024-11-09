from django.core.management.base import BaseCommand
from users.models import User, Profile

class Command(BaseCommand):
    help = 'Create an admin user and profile'

    def handle(self, *args, **kwargs):
        admin_user = User.objects.create_superuser(
            username="admin",
            email_address="admin@gmail.com",
            password="admin123",
            referred_by=None
            role="GS",
        )
        Profile.objects.create(
            user=admin_user,
            first_name="System",
            last_name="Admin",
            profile_picture=None,
            date_of_birth="1990-01-01",
            sex="M",
            batch_number="BSc - 25",
            registration_number="2024000000",
            hometown="Dhaka",
            phone_number="0170000000"
        )
        self.stdout.write(self.style.SUCCESS('Successfully created admin user and profile'))
