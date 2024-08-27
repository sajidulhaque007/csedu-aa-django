from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.core.exceptions import PermissionDenied, ValidationError
from mailing.models import SystemMail, UserMail
from mailing.serializers import SystemMailSerializer, UserMailSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class SystemMailList(ListAPIView):
    serializer_class = SystemMailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        queryset = SystemMail.objects.all()

        page_size = self.request.query_params.get('page_size', None)
        
        if page_size :
            self.pagination_class = PageNumberPagination
            self.pagination_class.page_size = int(page_size)
        else:
            self.pagination_class = None

        return queryset

class SystemMailDetail(RetrieveAPIView):
    queryset = SystemMail.objects.all()
    serializer_class = SystemMailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class UserMailList(ListAPIView):
    serializer_class = UserMailSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_queryset(self):
        queryset = UserMail.objects.all()

        # Get the sender username from query parameter
        sender_username = self.request.query_params.get('sender', None)
        if sender_username:
            queryset = queryset.filter(sender__username=sender_username)

        # Get the recipients username from query parameter
        recipient_username = self.request.query_params.get('recipient', None)
        if recipient_username:
            queryset = queryset.filter(recipients__username=recipient_username)

        queryset = queryset.filter(is_sent=True)

        page_size = self.request.query_params.get('page_size', None)
        
        if page_size :
            self.pagination_class = PageNumberPagination
            self.pagination_class.page_size = int(page_size)
        else:
            self.pagination_class = None

        return queryset

class UserMailDetail(RetrieveAPIView):
    queryset = UserMail.objects.all()
    serializer_class = UserMailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        obj = super().get_object()
        if not obj.sender == self.request.user:
            raise PermissionDenied('You are not authorized to access this mail.')
        return obj
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class UserSentMailList(ListAPIView):
    serializer_class = UserMailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = UserMail.objects.filter(sender=self.request.user)

        # Get the recipients username from query parameter
        recipient_username = self.request.query_params.get('recipient', None)
        if recipient_username:
            queryset = queryset.filter(recipients__username=recipient_username)

        queryset = queryset.filter(is_sent=True)

        page_size = self.request.query_params.get('page_size', None)
        
        if page_size :
            self.pagination_class = PageNumberPagination
            self.pagination_class.page_size = int(page_size)
        else:
            self.pagination_class = None

        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
