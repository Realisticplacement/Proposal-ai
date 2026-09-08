from rest_framework.permissions import BasePermission


class IsProposalOrganizationMember(BasePermission):

    def has_object_permission(self, request, view, obj):

        return (request.user.is_authenticated and obj.organization == request.user.organization)