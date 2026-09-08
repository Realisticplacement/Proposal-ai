from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Client
from .serializers import ClientSerializer
from .permissions import IsClientOwner

# Create your views here.


class ClientListCreateView(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Client.objects.filter(organization=self.request.user.organization)


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsClientOwner]

    def get_queryset(self):
        return Client.objects.filter(organization=self.request.user.organization)

    