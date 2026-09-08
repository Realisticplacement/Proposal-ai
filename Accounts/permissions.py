from rest_framework.permissions import BasePermission

# Custom permission to only allow members of an organization to access certain views.

class IsOrgannizationMember(BasePermission):

    def has_permission(self, request, view, obj):
        return (request.user.is_authenticated and obj.organization == request.user.organization)