from rest_framework import permissions
from events.models import Event

class IsEventManager(permissions.BasePermission):
    """
    Custom permission to only allow event managers to create event announcements.
    """

    def has_permission(self, request, view):
        event_id = view.kwargs.get('event_id')
        if event_id:
            event = Event.objects.get(pk=event_id)
            return request.user in event.managers.all()
        return False
