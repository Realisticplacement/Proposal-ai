from rest_framework.permissions import BasePermission

# Custom permission to only allow members of an organization to access an object.

class IsOrganizationMember(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and obj.organization == request.user.organization
        )


# Keep the old name available for existing imports.
IsOrgannizationMember = IsOrganizationMember