from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ValidationError
from django.shortcuts import get_object_or_404
from events.models import Event

class EventSubscriptionView(APIView):
    """
    API endpoint for subscribing to an event as a guest.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, event_id):
        # Check if event exists
        event = get_object_or_404(Event, pk=event_id)

        if request.user in event.managers.all():
            return Response({'detail': 'Managers cannot be subscribed as guests'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user is already attending the event
        if request.user in event.guests.all():
            raise ValidationError('User is already attending the event.')

        # Subscribe user as guest
        event.guests.add(request.user)
        event.save()

        return Response({'message': 'Successfully subscribed to event.'})
    
    def delete(self, request, event_id):
        # Check if event exists
        event = get_object_or_404(Event, pk=event_id)

        if request.user in event.guests.all():
            # Unsubscribe user from event
            event.guests.remove(request.user)
            event.save()
            return Response({'message': 'Successfully unsubscribed from event.'})
        else:
            raise NotFound('User is not attending the event.')

