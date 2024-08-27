from rest_framework import generics, permissions
from .models import Card
from .serializers import CardSerializer
from rest_framework.pagination import PageNumberPagination


class CardListCreateView(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return []

    def perform_create(self, serializer):
        serializer.save()
    
    def get_queryset(self):
        queryset = Card.objects.all()

        page_size = self.request.query_params.get('page_size', None)
        
        if page_size :
            self.pagination_class = PageNumberPagination
            self.pagination_class.page_size = int(page_size)
        else:
            self.pagination_class = None

        return queryset


class CardRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
