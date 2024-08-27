import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_referral_code():
    return str(uuid.uuid4().hex[:10])


class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    referral_code = models.CharField(max_length=10, unique=True, default=generate_referral_code)
    referred_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referrer.username}'s Referral ({self.referral_code})"
