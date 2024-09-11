from rest_framework.exceptions import ValidationError
from django.shortcuts import render
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from django.http import HttpResponse
from rest_framework.request import Request
from base.cache.redis import set_cache, get_cache
from .utils.token import create_tokens
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import json
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

class CurrentUserAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, pk=None, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response({'data': serializer.data, 'success': True})


class UsersAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)

        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response({'data': serializer.data, 'success': True})

    def post(self, request, format=None):
        # serializer = UserSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({'data': {'msg': 'Data Created'}, 'success': True}, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Send email to the registered user
            html_message = render_to_string('mailing/templates/registration_success.html', {'username': user.username})
            send_mail(
                subject='Welcome to the platform!',
                message='Hi {user.username}, thank you for registering.',  # Plain text fallback
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
)

            # Send email to admin
            send_mail(
                subject='New User Registration',
                message=f'A new user has registered with the username {user.username}.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['tahmid8017@gmail.com'],  # Replace with admin email
                fail_silently=False,
            )

            return Response({'data': {'msg': 'Data Created'}, 'success': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        id = pk
        user = User.objects.get(pk=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': {'msg': 'Data Updated'}, 'success': True}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        id = pk
        user = User.objects.get(pk=id)
        user.delete()
        return Response({'msg': 'Data Deleted'}, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([AllowAny])
def login(request: Request) -> Response:
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        raise ValidationError(
            detail='Username and password are required', code=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(username__exact=username)
        if not user.check_password(raw_password=password):
            raise ValidationError(detail='Invalid password', code=status.HTTP_400_BAD_REQUEST)

        access_token, refresh_token = create_tokens(user=user)
        
        # Render HTML email template
        html_message = render_to_string('mailing/templates/login_email.html', {
            'username': user.username,
            'site_name': 'cseduaa.org'  # You can replace this with your actual site name
        })
        
        # Send login email notification with HTML template
        send_mail(
            subject='Login Notification',
            message='You have logged into your account.',  # Plain text fallback
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,  # Use the rendered HTML message
            fail_silently=False,
        )
        
        data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
        set_cache(key=f'{username}_token_data', value=json.dumps(
            UserSerializer(user).data), ttl=5*60*60)
        
        return Response(data=data, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        raise ValidationError(detail='User not found', code=status.HTTP_404_NOT_FOUND)