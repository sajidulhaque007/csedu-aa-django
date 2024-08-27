from rest_framework import serializers

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        # Check if the current password and new password are the same
        if current_password == new_password:
            raise serializers.ValidationError("Current password and new password cannot be the same")

        return data
    
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get('email')
        token = data.get('token')
        new_password = data.get('new_password')

        return data