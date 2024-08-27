from rest_framework import serializers
from .models import SSLPayment

class SSLPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSLPayment
        fields = '__all__'
