from rest_framework.permissions import BasePermission
from .models import User
from rest_framework.views import Request, View


class IsAccountOwner(BasePermission):
    def has_object_permission(self, request: Request, _: View, obj: User):
        print(obj.password == request.user.password
              and obj.username == request.user.username or
              request.user.is_employee is True)
        if request.user.is_employee is True:
            return True

        return (obj.password == request.user.password
                and obj.username == request.user.username)
