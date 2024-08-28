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
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
            detail='username and password if required', code=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username__exact=username)
        if not user.check_password(raw_password=password):
            raise ValidationError(detail='invalid password',
                                  code=status.HTTP_400_BAD_REQUEST)
        access_token, refresh_token = create_tokens(user=user)
        data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
        set_cache(key=f'{username}_token_data', value=json.dumps(
            UserSerializer(user).data), ttl=5*60*60)
        return Response(data=data, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        raise ValidationError(detail='user not found',
                              code=status.HTTP_404_NOT_FOUND)
