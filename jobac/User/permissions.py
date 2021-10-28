from rest_framework import permissions



"""
    Checking permissions of our user groups
"""
class isEmployer(permissions.BasePermission):
    def has_permission(self, request):
        return bool(request.user and request.user.user_group == 2)


class IsFreelancer(permissions.BasePermission):
    def has_permission(self, request):
        return bool(request.user and request.user.user_group == 3)
