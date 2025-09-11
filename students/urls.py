from rest_framework.routers import DefaultRouter
from . views import StudentViewSet
from django.urls import path,include
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet

router= DefaultRouter ()
router.register(r"student", StudentViewSet, basename= "student")

urlpatterns = [
    path("", include (router.urls))
    ]
