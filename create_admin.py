import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from users.models import User, Profile


def create_admin():
    username = "admin"
    email = "admin@gmail.com"
    password = "admin123"

    if User.objects.filter(username=username).exists():
        print(f'User "{username}" already exists.')
    else:
        admin_user = User.objects.create_superuser(username=username, email_address=email, password=password)
        print(f'Superuser "{username}" created successfully.')

        profile = Profile.objects.create(
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
        print(f'Profile for "{username}" created successfully.')

if __name__ == "__main__":
    create_admin()