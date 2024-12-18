from django.urls import path
from .views import InitiatePaymentView, PaymentSuccessView, PaymentFailView ,PaymentCancelView, PaymentUsers

urlpatterns = [
    path('initiate/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('fail/', PaymentFailView.as_view(), name='payment-fail'),
    path('cancel/', PaymentCancelView.as_view(), name='payment-cancel'),
    path('users/', PaymentUsers.as_view(), name='payment-users'),
]
