from rest_framework import permissions

class IsStaffUser(permissions.BasePermission):
    """
    Permission for Staff Users to Can Change in Items of Product or etc...
    """

    def has_permission(self, request, view):  # list
        if request.method in permissions.SAFE_METHODS:  # get, head, option
            return True
        return request.user.is_staff
    
    def has_object_permission(self, request, view, obj):  # one object
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class IsOwnerUser(permissions.BasePermission):
    """
    Permission for Check User Send Request is Owner of Object or No
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.customer or request.user.is_staff
