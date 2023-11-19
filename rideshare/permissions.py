from rest_framework import permissions

class IsVerifiedAndRider(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_verified and request.user.user_type == 'rider':
            return True
        return False
    

class IsVerifiedAndPassanger(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_verified and request.user.user_type == 'passenger':
            return True
        return False