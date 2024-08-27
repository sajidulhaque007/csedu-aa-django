from django.urls import path
from .views import InitiatePaymentView, PaymentSuccessView, PaymentFailView

urlpatterns = [
    path('initiate/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('fail/', PaymentFailView.as_view(), name='payment-fail'),
]
