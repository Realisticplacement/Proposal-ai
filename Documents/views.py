from typing import cast

from Accounts.models import User
from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Document
from .serializers import DocumentSerializer
from .permissions import IsDocumentOrganizationMember

# Create your views here.

class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Document]:  # pyright: ignore[reportIncompatibleMethodOverride]
        user = cast(User, self.request.user)
        if user.organization is None:
            return Document.objects.none()
        return Document.objects.filter(organization=user.organization)

    def perform_create(self, serializer):
        user = cast(User, self.request.user)
        if user.organization is None:
            raise PermissionDenied('You must belong to an organization to upload a document.')
        serializer.save(organization=user.organization)


class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated, IsDocumentOrganizationMember]

    def get_queryset(self) -> QuerySet[Document]:  # pyright: ignore[reportIncompatibleMethodOverride]
        user = cast(User, self.request.user)
        if user.organization is None:
            return Document.objects.none()
        return Document.objects.filter(organization=user.organization)