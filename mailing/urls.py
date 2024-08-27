from django.urls import path
from mailing.views import SystemMailList, SystemMailDetail, UserMailList, UserMailDetail, SendEmailToUser, AdminSendEmailToMultipleUser, UserSentMailList

# Define URL patterns for different views
urlpatterns = [
    # URLs only accessible to admins
    path('system/', SystemMailList.as_view(), name='system-mail-list'), # Display a list of system-wide emails sent by admins
    path('system/<int:pk>/', SystemMailDetail.as_view(), name='system-mail-detail'), # Display details of a particular system-wide email
    path('admin-send/', AdminSendEmailToMultipleUser.as_view(), name='send-email-to-multiple-user'), # Display a form to send an email to multiple users

    # URLs accessible to both users and admins
    path('user/', UserMailList.as_view(), name='user-mail-list'), # Display a list of emails exchanged between users
    path('user/<int:pk>/', UserMailDetail.as_view(), name='user-mail-detail'), # Display details of a particular email exchanged between users
    path('send/<str:username>/', SendEmailToUser.as_view(), name='send-email-to-user'), # Display a form to send an email to a specific user
    path('sent-mails/', UserSentMailList.as_view(), name='user-sent-mail-list'), # Display a list of emails sent by the current user
]
