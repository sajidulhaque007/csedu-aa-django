from rest_framework import generics, permissions, status
from rest_framework.response import Response
from events.models import Event
from users.models import User
from rest_framework.exceptions import NotFound, PermissionDenied

class EventManagersAddAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_event(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise NotFound('Event not found.')

    def check_user_permission(self, event, user):
        if not event.managers.filter(pk=user.pk).exists():
            raise PermissionDenied('You do not have permission to manage this event.')

    def post(self, request, pk):
        event = self.get_event(pk)
        self.check_user_permission(event, request.user)

        usernames = request.data.get('usernames')

        if not isinstance(usernames, list):
            return Response({'detail': 'Usernames must be provided as a list.'}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(username__in=usernames)

        if len(users) != len(usernames):
            non_existing_usernames = set(usernames) - set(users.values_list('username', flat=True))
            return Response({'detail': f'Users {non_existing_usernames} do not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        event.managers.add(*users)
        return Response({'detail': 'Managers added successfully.'}, status=status.HTTP_200_OK)


class EventManagersDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_event(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise NotFound('Event not found.')

    def check_user_permission(self, event, user):
        if not event.managers.filter(pk=user.pk).exists():
            raise PermissionDenied('You do not have permission to manage this event.')

    def get_object(self):
        event = self.get_event(self.kwargs['pk'])
        self.check_user_permission(event, self.request.user)
        username = self.kwargs['username']
        try:
            user_to_remove = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound('User not found.')
        if user_to_remove == self.request.user:
            raise PermissionDenied('You cannot remove yourself from managers.')
        if user_to_remove == event.creator:
            raise PermissionDenied('You cannot remove the creator from managers.')
        if not event.managers.filter(pk=user_to_remove.pk).exists():
            raise NotFound('User is not a manager of this event.')
        return user_to_remove

    def delete(self, request, *args, **kwargs):
        event = self.get_event(self.kwargs['pk'])
        self.check_user_permission(event, self.request.user)
        return self.destroy(request, *args, **kwargs)

