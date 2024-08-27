from rest_framework import generics, permissions
from events.models import EventAnnouncement, Event
from events.serializers import EventAnnouncementSerializer
from events.permissions import IsEventManager
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ParseError


class EventAnnouncementListCreateView(generics.ListCreateAPIView):
    serializer_class = EventAnnouncementSerializer

    # Set permissions based on request method
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAuthenticated(), IsEventManager()]

    # Add request to serializer context
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        try:
            event_id = self.kwargs.get('event_id')
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            raise ParseError("Event does not exist")

        serializer.save(posted_by=self.request.user, event=event)

    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        event = get_object_or_404(Event, pk=event_id)
        queryset = EventAnnouncement.objects.filter(event=event)
        return queryset


class EventAnnouncementRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventAnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Only return announcements for the associated event
    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        return EventAnnouncement.objects.filter(event_id=event_id)

    # Only allow the user who posted the announcement to update it
    def perform_update(self, serializer):
        posted_by = serializer.validated_data.get('posted_by')
        if posted_by != self.request.user:
            raise permissions.PermissionDenied('You are not authorized to update this announcement.')
        serializer.save()

    # Only allow managers of the associated event to delete announcements
    def perform_destroy(self, instance):
        event = instance.event
        if self.request.user not in event.managers.all():
            raise permissions.PermissionDenied('You are not authorized to delete announcements for this event.')
        instance.delete()

    # Add request to serializer context
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
