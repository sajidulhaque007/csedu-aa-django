from rest_framework import serializers
from events.models import EventAnnouncement
from users.serializers import SmallUserCardSerializer

from rest_framework import serializers
from events.models import EventAnnouncement
from users.serializers import SmallUserCardSerializer

class EventAnnouncementSerializer(serializers.ModelSerializer):
    posted_by = SmallUserCardSerializer(read_only=True)
    can_edit = serializers.SerializerMethodField(read_only=True)
    can_delete = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = EventAnnouncement
        fields = ['id', 'text', 'picture', 'event', 'posted_by', 'created_at', 'updated_at', 'can_edit', 'can_delete']
        read_only_fields = ['id', 'posted_by', 'event']

    def get_can_edit(self, obj):
        request_user = self.context['request'].user
        return obj.posted_by == request_user

    def get_can_delete(self, obj):
        request_user = self.context['request'].user
        return request_user.is_authenticated and (obj.posted_by == request_user or request_user in obj.event.managers.all())

