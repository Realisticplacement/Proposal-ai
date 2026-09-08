from django.urls import path
from .views import (ClientListCreateView, ClientDetailView)


urlpatterns = [
    path('create-list/', ClientListCreateView.as_view(), name='client-list-create'),    
    path('<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
]

