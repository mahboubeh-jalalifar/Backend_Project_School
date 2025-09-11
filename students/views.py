from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.viewsets import ModelViewSet
from .models import StudentModel
from .serializers import StudentSerializer

class IsOwnerOrAdmin (permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff ():
            return True
        return getattr (obj, "user_id", None) == request.user.id

class StudentViewSet (viewsets.ModelViewSet):
    queryset= StudentModel.objects.all ()
    serializer_class = StudentSerializer ()

    def get_permissions (self):
        if self.action in ["destroy","list","update"]:
              return [permissions.IsAdminUser ()]
        return [permissions.IsAuthenticated(), IsOwnerOrAdmin ()]
