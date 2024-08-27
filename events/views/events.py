from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from events.models import Event
from events.serializers import EventSerializer, EventListSerializer
from events.managers import EventManager

class ListCreateEventAPI(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    pagination_class = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-start_datetime', 'end_datetime', 'pk')
        page_size = self.request.query_params.get('page_size', None)
        
        if page_size:
            self.pagination_class = PageNumberPagination
            self.pagination_class.page_size = int(page_size)
        
        return queryset
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return (permissions.IsAuthenticated(),)
        elif self.request.method == 'POST':
            if not self.request.user.is_authenticated:
                raise PermissionDenied('Authentication credentials were not provided.')
            elif not self.request.user.is_admin:
                raise PermissionDenied('Only admin users can create events.')
            return (permissions.IsAuthenticated(),)

    def perform_create(self, serializer):
        creator = self.request.user if self.request.user.is_admin else None
        event = EventManager().create(creator=creator, **serializer.validated_data)
        serializer.instance = event

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows managers to update an event, and the creator/superuser to delete an event.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def check_permissions(self, request):
        """
        Check if the user has the necessary permissions to perform the requested action.
        """
        event = self.get_object()

        if request.method == 'DELETE':
            if not (request.user == event.creator or request.user.is_superuser):
                raise PermissionDenied('You do not have permission to delete this event.')

        if request.method in ('PUT', 'PATCH'):
            if not event.managers.filter(pk=request.user.pk).exists():
                raise PermissionDenied('Only managers can update this event.')

        super().check_permissions(request)

    def delete(self, request, *args, **kwargs):
        event = self.get_object()
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)