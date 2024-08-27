# Generated by Django 4.1.3 on 2023-04-11 15:33

from django.db import migrations, models
import users.models.user


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_workexperience_socialmedialink_skill_presentaddress_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, unique=True, validators=[users.models.user.User.validate_username]),
        ),
    ]
