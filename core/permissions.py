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
