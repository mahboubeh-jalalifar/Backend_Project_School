from django.shortcuts import render
from rest_framework import permissions,viewsets, status, decorators
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from .models import Course, Class , Lesson, Enrollment, Attendance
from .serializers import CourseSerializer, ClassListSerializer, ClassSerializer, LessonSerializer, EnrollmentSerializer, AttendanceSerializer
from rest_framework.response import Response
from django.db.models import Q


class CourseViewSet (viewsets.ModelViewSet):
    queryset= Course.objects.all ()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ["list","destroy","update","partial_update","create"]:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
class IsTeacherOwnerOrAdminUser (permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return getattr (obj,"teacher_profile",None) == request.user.teacher_profile

class IsEnrolledOrTeacherOrAdmin (permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if hasattr (request.user, "teacher_profile"):
            return obj.teacher==request.user.teacher_profile
        if hasattr (request.user, "student_profile"):
            return obj.enrollments.filter (student=request.user.student_profile,is_active=True).exists()
        

class ClassViewSet (viewsets.ModelViewSet):
    queryset = Class.objects.select_related ("teacher__user", "course","lesson").filter(is_active= True)

    def get_serializer_class(self):
        if self.action in ["list"]:
            return ClassListSerializer
        elif self.action in ["retrieve"]:
            return ClassSerializer
        
    def get_permissions(self):
        if self.action in ["update","partial_update","create","destroy"]:
            return [permissions.IsAuthenticated(), IsTeacherOwnerOrAdminUser ()]
        elif self.action in ["list","retrieve","enrollment","lesson"]:
            return [permissions.IsAuthenticated(),IsEnrolledOrTeacherOrAdmin()]
        
    def get_queryset(self):
        user= self.request.user
        queryset= self.queryset

        if hasattr (user,"teacher_profile") and not user.is_staff:
            queryset= queryset.filter (teacher=user.teacher_profile)
        elif hasattr (user,"student_profile") and not user.is_staff :
            queryset= queryset.filter (enrollments__student= user.student_profile,
                                       enrollments__is_active=True)
        
        return queryset
        
    def perform_create(self, serializer):
        if getattr (self.request.user, "teacher_profile", None) and not self.request.user.is_staff :
            return serializer.save (teacher= self.request.user.teacher_profile)
        else:
            return serializer.save()
        
    @action (detail=True, methods=["get"])
    def lessons (self, request, pk=None):
        class_instance= self.get_object ()
        lessons= class_instance.lessons.all().order_by("schedule")
        serializer= LessonSerializer (lessons, many= True)
        return Response (serializer.data)

    @action (detail=True, methods=["get"])
    def enrollments (self, request, pk= None):
        class_instance= self.get_object ()

        if not (request.user.is_staff or
            (hasattr (request.user, "teacher_profile") and
            class_instance.teacher== request.user.teacher_profile)):
            return Response ({"error":"permission denied"}, status= status.HTTP_403_FORBIDDEN)

        enrollments= class_instance.enrollments.filter(is_active=True).order_by("date")
        serializer= EnrollmentSerializer (enrollments, many=True)
        return Response (serializer.data)

    @action (detail=True, methods=["post"])
    def enroll (self, request, pk=None):
        if not hasattr (request.user, "student_profile"):
            return Response ({"error":"Only satudents can enroll in class"},
                              status=status.HTTP_403_FORBIDDEN)
        
        class_instance= self.get_object ()
        data= {"class_id": class_instance.id}
        serializer= EnrollmentSerializer (data= data , context={"request": request})

        if serializer.is_valid () :
            serializer.save (student= request.user.student_profile, class_instance= class_instance)
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_403_FORBIDDEN)

    @action (detail=True, methods=["post"])
    def unenroll (self, request, pk= None):
        if not hasattr (request.user, "student_profile"):
            return Response ({"error": "only students can unenroll"}, status=status.HTTP_403_FORBIDDEN)
        
        class_instance= self.get_object ()
        try:
            enrollment= Enrollment.objects.get (
                student=request.user.student_profile,
                class_instance=class_instance,
                is_active=True)
            enrollment.is_active=False
            enrollment.save()
            return Response ({"message":"action is done successfuly"}
                             ,status=status.HTTP_201_CREATED)
        
        except Enrollment.DoesNotExist:
            return Response({"error":"You are not enrolled in this class"}
                            , status=status.HTTP_403_FORBIDDEN)
            

class LessonViewSet(viewsets.ModelViewSet):
    serializer_class= LessonSerializer

    def get_queryset(self):
        user= self.request.user
        if hasattr (user, "teacher_profile") and not user.is_staff :
            return Lesson.objects.filter (class_instance__teacher= user.teacher_profile)
        elif hasattr (user, "student_profile") and not user.is_staff :
            return Lesson.objects.filter (
                class_instance__enrollments__student= user.student_profile,
                class_instance__enrollments__is_active=True)
        
        return Lesson.objects.all ()
    
    def get_permissions(self):
        if self.action in ["create","update","partial_update","destroy"]:
            return [permissions.IsAuthenticated(), IsTeacherOwnerOrAdminUser()]
        return [permissions.IsAuthenticated()]
    
    @action (detail=True, methods=["get","post"])
    def attendance (self, request, pk=None):
        lesson= self.get_object ()

        if request.method == "GET":
            attendance= lesson.lesson_attendance.all ()
            serializer= AttendanceSerializer (attendance, many=True)
            return Response (serializer.data)
        
        elif request.method == "POST":
            if not (request.user.is_staff or (hasattr (request.user, "teacher_profile") and
              lesson.class_instance.teacher == request.user.teacher_profile)):
                return Response({"error message": "Permission denied"},
                                 status=status.HTTP_403_FORBIDDEN)
            
            
            attendance_data = request.data.get("attendance", [])
            for item in attendance_data:
                item["lesson"] = lesson.id
                serializer = AttendanceSerializer(data=item)
                if serializer.is_valid():
                    Attendance.objects.update_or_create(
                        lesson=lesson,
                        student_id=item["student"],
                        defaults={
                            "status": item["status"],
                            "note": item.get("note", "")
                        }
                    )
            
            return Response({"message": "Attendance recorded successfully"})
        
class EnrollmentViewSet (viewsets.ModelViewSet):
    serializer_class= EnrollmentSerializer

    def get_queryset(self):
        user= self.request.user 
        if hasattr (user, "student_profile") and not user.is_staff:
            return Enrollment.objects.filter (student= user.student_profile,is_active=True)
        
        if hasattr (user, "teacher_profile") and not user.is_staff :
            return Enrollment.objects.filter (class_instance__teacher= user.teacher_profile,is_active=True)
        
    def get_permissions(self):
        if self.action in ["create"]:
            return [permissions.IsAuthenticated()]
        if self.action in ["update","partial_update","destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        if hasattr (self.request.user, "student_profile") and not self.request.user.is_staff :
            serializer.save (student= self.request.user.student_profile)
        else:
            return serializer.save()


            
