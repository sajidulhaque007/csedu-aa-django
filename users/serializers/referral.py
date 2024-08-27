from rest_framework import serializers
from users.models import Referral
from users.serializers import SmallUserCardSerializer
class ReferralSerializer(serializers.ModelSerializer):
    referrer = SmallUserCardSerializer(read_only = True)
    class Meta:
        model = Referral
        fields = ['referrer', 'referral_code', 'referred_email', 'created_at']
        read_only_fields = ['referrer', 'referral_code', 'created_at']
