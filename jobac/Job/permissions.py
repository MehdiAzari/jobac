from rest_framework import permissions


class IsOwnerOfJob(permissions.BasePermission):

    def has_object_permission(self, request,_, obj):
        return obj.employer.user == request.user

