from rest_framework import serializers
from mailing.models import SystemMail, UserMail
from users.serializers import SmallUserCardSerializer
from mailing.serializers.email import CommonEmailAddressSerializer

class SystemMailSerializer(serializers.ModelSerializer):
    sender = SmallUserCardSerializer(read_only = True)
    recipients = CommonEmailAddressSerializer(read_only = True, many = True)

    class Meta:
        model = SystemMail
        fields = '__all__'
    
    def to_representation(self, instance):
        """
        Override the default to_representation method to hide the body of private mails.
        """
        data = super().to_representation(instance)
        if instance.is_mail_private:
            data['body'] = 'This mail is marked as private.'
        return data

class UserMailSerializer(serializers.ModelSerializer):
    sender = SmallUserCardSerializer(read_only=True)
    recipients = SmallUserCardSerializer(many=True, read_only=True)

    class Meta:
        model = UserMail
        fields = '__all__'

    def to_representation(self, instance):
        """
        Override the default to_representation method to hide the body of private mails.
        """
        request = self.context.get('request')
        data = super().to_representation(instance)
        if instance.is_mail_private and (not request.user == instance.sender):
            data['body'] = 'This mail is marked as private.'
        return data


class UserMailSendingSerializer(serializers.ModelSerializer):
    is_mail_private = serializers.BooleanField(required=False)

    class Meta:
        model = UserMail
        fields = ['subject', 'body', 'is_mail_private']

class UserMailMultipleSendingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserMail
        fields = ['subject', 'body']