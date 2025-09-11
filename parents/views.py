from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.viewsets import ModelViewSet
from .models import ParentsModel
from .serializers import ParentsSerializer

class IsAdminOrOwner (permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff ():
         return True
        return getattr(obj,"user_id",None) == request.user.id
        
class ParentViewSet (viewsets.ModelViewSet):
    queryset= ParentsModel.objects.all()
    serializer_class= ParentsSerializer
    
    def get_permissions(self):
        if self.action in ["list","read","update","destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated(), IsAdminOrOwner()]
