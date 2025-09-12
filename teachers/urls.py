from .views import TeacherViewSet
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router= DefaultRouter ()
router.register (r"teachers", TeacherViewSet, basename= "teachers")

urlpatterns = [
    path ("", include (router.urls))
]