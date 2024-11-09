from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from users.models import Referral, User
from users.serializers import ReferralSerializer, ChangePasswordSerializer, ResetPasswordSerializer, UserSerializer
from users.managers import UserManager
from mailing.models import SystemMailManager
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
import logging
from users.models.choices import ROLE_CHOICES
import pyrebase
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from users.models import User
from base.models import BaseModel
from mailing.models.email import CommonEmailAddress
import smtplib, re
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)
# Initialize Firebase
firebase_config = {
  'apiKey': 'AIzaSyD2aYx8IBIK2Itef4UVfZKNYVmHpkZznVI',
  'authDomain': 'cseduaa-c1a30.firebaseapp.com',
  'projectId': 'cseduaa-c1a30',
  'storageBucket': 'cseduaa-c1a30.appspot.com',
  'messagingSenderId': '137515276822',
  'appId': '1:137515276822:web:0debdc77bf4373ca63f337',
  "databaseURL": "https://cseduaa-c1a30.firebaseio.com"

}
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

@csrf_exempt
def google_signin(request):
    if request.method == "POST":
        try:
            # Log the request body to debug
            print("Request body:", request.body)
            
            # Parse request body
            body = json.loads(request.body.decode('utf-8'))
            id_token = body.get('idToken')
            
            if not id_token:
                return JsonResponse({"error": "No token provided"}, status=400)

            # Verify the ID token with Firebase
            decoded_token = auth.get_account_info(id_token)
            email_address = decoded_token['users'][0]['email']

            # Check if the user already exists in the Django backend
            try:
                user = User.objects.get(email_address=email_address)  # Use email_address field instead of email
            except User.DoesNotExist:
                user = User.objects.create(
                    username=email_address,
                    email_address=email_address,
                    password=user.set_password(email_address)   # Set a random password for Google users
                )          
            token, _ = Token.objects.get_or_create(user=user)
            return JsonResponse({
                "message": "Sign-in successful",
                "token": token.key,
                "user": {
                    "username": user.username,
                    "email_address": user.email_address, 
                    "password": user.password,# Return email_address in the response
                }
            })
        except Exception as e:
            print("Error:", str(e))  # Log the error for debugging
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def obtain_auth_token(request):
    """
    Obtain a token for a user and send an email on successful login.
    """
    timestamp = timezone.now()
    username = request.data.get("username")
    email_address = request.data.get("email")
    password = request.data.get("password")
    if username:
        user = authenticate(username=username, password=password)
    elif email_address:
        try:
            user = User.objects.get(email_address=email_address)
        except User.DoesNotExist:
            user = None
        if user and not user.check_password(password):
            user = None
    else:
        user = None
    if not user:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
    token, created = Token.objects.get_or_create(user=user)
    try:
        subject = 'Login Successful'
        body = render_to_string('login_success.html', {
            'user': user,
            'timestamp': timestamp
        })
        # send_mail(
        #     subject,
        #     body,
        #     'contact@cseduaa.org',  # Sender email
        #     [user.email_address],  # Recipient email
        #     fail_silently=False,
        # )
    except Exception as e:
        return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({'token': token.key})


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Logout the user by deleting their token.
    """
    request.auth.delete()
    return Response({'detail': 'Successfully logged out.'})


class ReferralCreate(APIView):
    queryset = Referral.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = ReferralSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        referral = serializer.save(referrer=self.request.user)
        referred_email = referral.referred_email
        referral_code = referral.referral_code
        referrer_first_name = referral.referrer.profile.first_name
        referrer_last_name = referral.referrer.profile.last_name

        # Send email to referred user
        mail_manager = SystemMailManager()
        sender = self.request.user
        recipients = [referred_email]
        subject = 'You have been referred!'
        context = {
            'referral_code': referral_code,
            'referrer_first_name' : referrer_first_name,
            'referrer_last_name' : referrer_last_name,
            }
        body = render_to_string('referral_email.html', context)
        logger.debug(f"Sender: {sender}")
        try:
            mail_manager.create_and_send_mail(sender, recipients, subject, body)
        except Exception as e:
            referral.delete()
            logger.error(str(e), exc_info=True, extra={'request': self.request})
            return Response({'error': 'An error occurred while sending the email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Send success message to requesting user
        return Response({'message': 'Referral sent successfully!'})


class ResetPassword(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email_address=email)
        except:
            return Response({'error': 'This user does not exist'}, status=status.HTTP_404_NOT_FOUND)

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        # Send email to referred user
        mail_manager = SystemMailManager()
        sender = User.objects.filter(role='GS').first()
        recipients = [email]
        subject = 'You requested a password reset'
        context = {
            'username': user.username,
            'token': token,
            }
        body = render_to_string('reset_email.html', context)
        try:
            mail_manager.create_and_send_mail(sender, recipients, subject, body)
        except Exception as e:
            logger.error(str(e), exc_info=True, extra={'request': self.request})
            return Response({'error': 'An error occurred while sending the email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Send success message to requesting user
        return Response({'message': 'Email sent successfully!'})

class ResetPasswordConfirmation(APIView):
    def put(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']

            try:
                user = User.objects.get(email_address=email)
            except:
                return Response({'error': 'This user does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
            token_generator = PasswordResetTokenGenerator()
            is_valid = token_generator.check_token(user, token)
            
            if is_valid:
                try:
                    user_manager = User.objects
                    user_manager.reset_password(user, new_password)
                    return Response({'success': 'Password changed successfully'}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]  # Set the permission class to IsAuthenticated

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']

            user = request.user

            # Update the user's password using the User Manager
            try:
                user_manager = User.objects
                user_manager.change_password(user, current_password, new_password)
                return Response({'success': 'Password changed successfully'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_admin(request):
    """
    API endpoint to make a user an admin.
    Only superusers and admins can access this method.
    """
    try:
        # Get username from request
        username = request.data.get('username')
        
        # Check if username is provided
        if not username:
            return Response({'error': 'username is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user exists
        user = User.objects.get(username=username)
        
        # Check if the logged in user is an admin
        if not request.user.is_superuser and not request.user.is_admin:
            return Response({'error': 'Only superusers and admins can make a user an admin'}, status=status.HTTP_403_FORBIDDEN)
        
        # Make user an admin
        UserManager().make_user_admin(user)
        
        # Serialize and return user data
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_admin(request, username):
    """
    API endpoint to remove adminship from a user.
    Only superusers can access this method.
    """
    try:
        # Check if user exists
        user = User.objects.get(username=username)
        
        # Check if the logged in user is a superuser
        if not request.user.is_superuser:
            return Response({'error': 'Only superusers can remove adminship from a user'}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if user is a superuser
        if user.is_superuser:
            return Response({'error': 'Cannot remove adminship from a superuser'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Remove adminship from user
        UserManager().remove_user_adminship(user)
        
        # Serialize and return user data
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_role(request):
    """
    API endpoint to set a user's role.
    Only superusers and admins can access this method.
    """
    try:
        # Get username and role from request
        username = request.data.get('username')
        role = request.data.get('role')
        
        # Check if username and role are provided
        if not username or not role:
            return Response({'error': 'username and role are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if role is valid
        valid_roles = [choice[0] for choice in ROLE_CHOICES]
        if role not in valid_roles:
            return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user exists
        user = User.objects.get(username=username)
        
        # Check if the logged in user is an admin or superuser
        if not request.user.is_superuser and not request.user.is_admin:
            return Response({'error': 'Only superusers and admins can set a user role'}, status=status.HTTP_403_FORBIDDEN)
        
        # Set user's role
        user.role = role
        user.save()
        
        # Serialize and return user data
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_pending(request, username):
    """
    API endpoint to accept or decline a pending user.
    Only superusers can access this method.
    """
    try:
        # Check if user exists
        user = User.objects.get(username=username)

        is_accepted = request.data.get("accept")
        
        if is_accepted:
            # Remove adminship from user
            UserManager().accept_pending(user)
        else:
            user.delete()
        
        # Serialize and return user data
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
