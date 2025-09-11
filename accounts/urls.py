from django.urls import path,include
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import UserModelViewSet
from rest_framework.routers import DefaultRouter

router= DefaultRouter ()
router.register (r"users",UserModelViewSet,basename="user")


urlpatterns = [
    path('',include (router.urls)),
    path ('token/obtain/', TokenObtainPairView.as_view(), name= 'Token_Obtain'),
    path ('token/refresh/', TokenRefreshView.as_view(), name= 'Token_Refresh'),
    
]
