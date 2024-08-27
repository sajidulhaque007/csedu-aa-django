from rest_framework import serializers
from .models import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'photo', 'title', 'caption', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
