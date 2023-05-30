from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsEmployeeOrReadOnly2(BasePermission):
    def has_permission(self, request, _):
        return (
            request.method in SAFE_METHODS or
            request.user.is_authenticated and
            request.user.is_employee)
