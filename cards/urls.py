from django.urls import path
from .views import CardListCreateView, CardRetrieveUpdateDeleteView


urlpatterns = [
    path('', CardListCreateView.as_view(), name='card-list-create'),
    path('<int:pk>/', CardRetrieveUpdateDeleteView.as_view(), name='card-retrieve-update-delete'),
]
