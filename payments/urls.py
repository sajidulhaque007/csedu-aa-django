from django.urls import path
from payments.views.views import PaymentCreateView, PaymentListView, PaymentDeleteView

urlpatterns = [
    path('payments-list/', PaymentListView.as_view(), name='payment-list'),
    path('create-payment/', PaymentCreateView.as_view(), name='create-payment'),
    path('delete-payment/<int:pk>/', PaymentDeleteView.as_view(), name='delete-payment'),
]