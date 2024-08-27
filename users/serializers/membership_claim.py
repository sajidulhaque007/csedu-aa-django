from rest_framework import serializers
from users.models import MembershipClaim
from users.serializers import SmallUserCardSerializer

class MembershipClaimSerializer(serializers.ModelSerializer):
    claimaint = SmallUserCardSerializer(read_only = True)
    class Meta:
        model = MembershipClaim
        fields = ['id', 'claimant', 'category', 'amount_paid', 'date_of_registration', 'proof_of_registration']
        read_only_fields = ['claimant']