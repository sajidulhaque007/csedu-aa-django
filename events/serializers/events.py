from rest_framework import serializers
from events.models import Event
from users.serializers import SmallUserCardSerializer
from events.serializers.announcement import EventAnnouncementSerializer


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event model.
    """
    managers = SmallUserCardSerializer(many=True, read_only=True)
    guests = SmallUserCardSerializer(many=True, read_only=True)
    creator = SmallUserCardSerializer(read_only=True)
    is_manager = serializers.SerializerMethodField(read_only=True)
    is_subscriber = serializers.SerializerMethodField(read_only=True)
    is_creator_or_superuser = serializers.SerializerMethodField(read_only=True)
    guest_count = serializers.SerializerMethodField(read_only=True)
    manager_count = serializers.SerializerMethodField(read_only=True)
    announcements = EventAnnouncementSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'

    def get_is_manager(self, obj):
        """
        Returns True if the request user is a manager of the event, False otherwise.
        """
        request_user = self.context['request'].user
        return request_user.is_authenticated and obj.managers.filter(pk=request_user.pk).exists()

    def get_is_subscriber(self, obj):
        """
        Returns True if the request user is a subscriber to the event, False otherwise.
        """
        request_user = self.context['request'].user
        return request_user.is_authenticated and obj.guests.filter(pk=request_user.pk).exists()

    def get_is_creator_or_superuser(self, obj):
        """
        Returns True if the request user is the creator of the event or a superuser, False otherwise.
        """
        request_user = self.context['request'].user
        return request_user.is_authenticated and (obj.creator == request_user or request_user.is_superuser)

    def get_guest_count(self, obj):
        """
        Returns the number of guests attending the event.
        """
        return obj.guests.count()
    
    def get_manager_count(self, obj):
        """
        Returns the number of managers of the event.
        """
        return obj.managers.count()

class EventListSerializer(EventSerializer):
    """
    Serializer for list of events without managers, guests, and announcements.
    """
    guests = None
    announcements = None

    class Meta:
        model = Event
        exclude = ['guests']
