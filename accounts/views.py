from django.shortcuts import render

from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.viewsets import ModelViewSet
from .serializers import UserModelSerializer
from rest_framework.response import Response
from .models import UserModel

class IsOwnerOradmin (permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff():
            return True
        return getattr(obj,"user_id",None) == request.user.id

class UserModelViewSet (viewsets.ModelViewSet):
    queryset = UserModel.objects.all ()
    serializer_class = UserModelSerializer 

    def get (self):
        user = UserModel.objects.all ()
        serializer = UserModelSerializer (user, many=True)
        return Response (serializer.data)
    
    def post (self,request):
        serializer= UserModelSerializer (data=request.data)
        if serializer.is_valid():
            serializer.save ()
            return Response(serializer.data ,status=status.HTTP_201_CREATED)
        else:
            return Response (serializer.data,status=status.HTTP_204_NO_CONTENT)

    def permissions (self):
        if self.action in ['create']:
            return [permissions.AllowAny()]
        elif self.action in ['destroy','list']:
            return [permissions.IsAdminUser()]
        else:
            return [permissions.IsAdminUser()],[permissions.IsAuthenticated(),IsOwnerOradmin()]





