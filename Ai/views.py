from typing import cast

from Accounts.models import User
from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .serializers import AIExecutionSerializer
from .models import AIExecution


class AIExecutionListView(generics.ListCreateAPIView):
    serializer_class = AIExecutionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[AIExecution]:  # pyright: ignore[reportIncompatibleMethodOverride]
        organization = cast(User, self.request.user).organization
        if organization is None:
            return AIExecution.objects.none()
        return AIExecution.objects.filter(organization=organization)

    def perform_create(self, serializer):
        organization = cast(User, self.request.user).organization
        if organization is None:
            raise PermissionDenied('You must belong to an organization to create an AI execution.')
        serializer.save(organization=organization)


class AIExecutionDetailView(generics.RetrieveAPIView):
    serializer_class = AIExecutionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[AIExecution]:  # pyright: ignore[reportIncompatibleMethodOverride]
        organization = cast(User, self.request.user).organization
        if organization is None:
            return AIExecution.objects.none()
        return AIExecution.objects.filter(organization=organization)

