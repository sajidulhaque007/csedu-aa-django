from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from mailing.models import UserMail, SystemMail
from mailing.serializers import UserMailSendingSerializer, UserMailMultipleSendingSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

class SendEmailToUser(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, username):
        try:
            recipient = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response({'error': 'Recipient not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserMailSendingSerializer(data=request.data)
        if serializer.is_valid():
            sender = request.user
            subject = serializer.validated_data['subject']
            body = serializer.validated_data['body']

            body = render_to_string('user_email.html', context = {
                'body': body,
                'sender_info' : f'{sender.profile.first_name} {sender.profile.last_name} from Batch {sender.profile.batch_number}',
            })

            is_mail_private = serializer.validated_data.get('is_mail_private', True)
            
            try:
                mail = UserMail.objects.create_and_send_mail(sender=sender, usernames=[recipient.username], subject=subject, body=body, is_mail_private=is_mail_private)
                serialized_mail = UserMailSendingSerializer(mail)
                return Response(serialized_mail.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminSendEmailToMultipleUser(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        recipient_usernames = request.data.pop('recipients', [])
        serializer = UserMailSendingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sender = request.user
        subject = serializer.validated_data['subject']
        body = serializer.validated_data['body']
        body = render_to_string('admin_email.html', context = {
                'body': body,
                'sender_info' : f'{sender.profile.first_name} {sender.profile.last_name} from Batch {sender.profile.batch_number}',
            })
        recipients = []
        for username in recipient_usernames:
            recipient = get_object_or_404(User, username=username)
            recipients.append(recipient)

        if not recipients:
            raise NotFound('No valid recipients found')

        try:
            logger.debug(f"Sender: {sender}")

            mail = UserMail.objects.create_and_send_mail(
                sender = sender, usernames=[recipient.username for recipient in recipients], subject=subject, body=body, is_mail_private=False)
            serialized_mail = UserMailMultipleSendingSerializer(mail)
            return Response(serialized_mail.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)