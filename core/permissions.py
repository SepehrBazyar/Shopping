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


class IsOwnerSite(permissions.BasePermission):
    """
    Permission for Check User is Owner Admin for Show List of Private Data
    """

    def has_permission(self, request, view):
        return request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class IsCustomerUser(permissions.BasePermission):
    """
    Permission for Check User Send Request is Self if not Forbidden
    """

    def has_object_permission(self, request, view, obj):
        return request.user.username == obj.username or request.user.is_staff


class IsOwnerUser(permissions.BasePermission):
    """
    Permission for Check User Send Request is Owner of Object if not Forbidden
    """

    def has_object_permission(self, request, view, obj):
        return request.user.username == obj.customer.username or request.user.is_staff


class IsCustomerOwnerParent(permissions.BasePermission):
    """
    Permission for Check User Send Request is Owner of Parent of tis Object
    """

    def has_object_permission(self, request, view, obj):
        return request.user.username == obj.order.customer.username or request.user.is_staff


class IsStaffAuthenticated(permissions.BasePermission):
    """
    Access for Create Just Staff User and Safe Methods Just for Authentiated Users
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            if request.method in permissions.SAFE_METHODS:
                return True
        return False


class IsCustomerOwner(permissions.BasePermission):
    """
    Access for Create New Object for Only Customers & Staff Users Just Can See List
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if not request.user.is_staff:
                return True
            elif request.method in permissions.SAFE_METHODS:
                return True
        return False
