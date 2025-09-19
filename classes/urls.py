from rest_framework.routers import DefaultRouter
from .views import ClassViewSet, CourseViewSet, LessonViewSet, EnrollmentViewSet
from django.urls import path,include

router= DefaultRouter ()
router.register (r"courses", CourseViewSet, basename="course")
router.register (r"classes",ClassViewSet, basename="class")
router.register (r"lessons",LessonViewSet, basename="lesson")
router.register (r"enrollments", EnrollmentViewSet, basename="enrollment")

urlpatterns = [
    path ("", include (router.urls)),
]

