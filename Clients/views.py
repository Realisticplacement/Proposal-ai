from typing import cast

from Accounts.models import User
from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Client
from .serializers import ClientSerializer
from .permissions import IsClientOwner

# Create your views here.


class ClientListCreateView(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Client]:  # pyright: ignore[reportIncompatibleMethodOverride]
        user = cast(User, self.request.user)
        if user.organization is None:
            return Client.objects.none()
        return Client.objects.filter(organization=user.organization)

    def perform_create(self, serializer):
        user = cast(User, self.request.user)
        if user.organization is None:
            raise PermissionDenied('You must belong to an organization to create a client.')
        serializer.save(organization=user.organization)


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsClientOwner]

    def get_queryset(self) -> QuerySet[Client]:  # pyright: ignore[reportIncompatibleMethodOverride]
        user = cast(User, self.request.user)
        if user.organization is None:
            return Client.objects.none()
        return Client.objects.filter(organization=user.organization)

    