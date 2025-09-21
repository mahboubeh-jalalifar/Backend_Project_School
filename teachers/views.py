from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.viewsets import ModelViewSet
from .models import TeacherModel
from .serializers import TeacherSerializer

class IsOwnerOrAdmin (permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return getattr (obj,"user_id",None) == request.user.id

class TeacherViewSet (viewsets.ModelViewSet):
    queryset= TeacherModel.objects.select_related ("user").all ()
    serializer_class = TeacherSerializer 

    def get_permissions(self):
        if self.action in ["destroy","list"]:
            return [permissions.IsAdminUser()]
        elif self.action in ["retrieve","partial_update","update"]:
            return [permissions.IsAuthenticated(),IsOwnerOrAdmin()]
        else:
            return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        user = self.request.user if not self.request.user.is_staff else serializer.validated_data.get ("user", self.request.user)
        serializer.save(user=user)
