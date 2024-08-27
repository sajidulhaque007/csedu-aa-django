from django.db import models
from django.contrib.auth import get_user_model
from users.models.choices import CLAIMANT_CHOICES
from django.core.validators import MinValueValidator

User = get_user_model()

class MembershipClaim(models.Model):
    claimant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='membership_claims')
    category = models.CharField(max_length=16, choices=CLAIMANT_CHOICES)
    amount_paid = models.IntegerField(validators=[MinValueValidator(0)])
    date_of_registration = models.DateTimeField()
    proof_of_registration = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.claimant.username}'s Claim for {self.category}"
