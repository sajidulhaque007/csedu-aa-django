from rest_framework import serializers
from payments.models.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'event', 'deadline', 'amount']