from rest_framework import serializers
from mailing.models import CommonEmailAddress
from users.serializers import SmallUserCardSerializer

class CommonEmailAddressSerializer(serializers.ModelSerializer):
    user = SmallUserCardSerializer(read_only=True, source='get_user')

    class Meta:
        model = CommonEmailAddress
        fields = ['email', 'user']

    # def to_representation(self, instance):
    #     """
    #     Override the default to_representation method to exclude user information if the user doesn't exist.
    #     """
    #     data = super().to_representation(instance)
    #     # if not instance.has_user():
    #     #     data.pop('user')
    #     return data