from rest_framework import permissions
from .models import GroupMembership , Group
from django.contrib.auth.models import User


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='manager').exists()


class IsDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        delivery_crew = Group.objects.get(name='delivery_crew') 
        user = User.objects.get(id=request.user.id)
        delivery = GroupMembership.objects.filter(user=user).exists()
        return delivery