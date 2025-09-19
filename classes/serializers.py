from rest_framework import serializers
from .models import Lesson, Course , Class, Enrollment, Attendance
from teachers.serializers import TeacherSerializer
from students.serializers import StudentSerializer
from django.core.exceptions import ValidationError

class CourseSerializer (serializers.ModelSerializer):
    class Meta:
        model = Course
        fields= ["id","code","title","description","lesson_type", "start_date","end_date","prerequisites","price","discount","is_free","rate","credits","score"]
        read_only_fields= ["id"]

    def create(self, validated_data):
        course= Course.objects.create (**validated_data)
        return course
        
    
class LessonSerializer (serializers.ModelSerializer):
    class Meta:
        model= Lesson
        fields = ["id","code","title","description","start_date","end_date","grade","prerequisites","credits","semester","schedule","duration","lesson_type","material","score"]
        read_only_fields= ["id"]

    def create (self,validated_data):
        lesson= Lesson.objects.create(**validated_data)
        return lesson

class ClassSerializer (serializers.ModelSerializer):
    teacher= TeacherSerializer (read_only= True)
    course= CourseSerializer (read_only= True)
    teacher_id= serializers.CharField (write_only= True)
    course_id= serializers.CharField(write_only= True)
    lesson_id= serializers.CharField(write_only=True)

    class Meta:
        model = Class 
        fields= ["id","name","course","teacher","room_number","building","is_active","capacity","teacher_id","course_id","lesson_id"]
        read_only_fields= ["id"]

    def create(self, validated_data):
        teacher_id = validated_data.pop("teacher_id")
        course_id = validated_data.pop("course_id")
        class_validate= Class.objects.create(
            teacher_id=teacher_id,
            course_id=course_id,
            **validated_data
        )
        return class_validate

class ClassListSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source="teacher.user.get_full_name", read_only=True)
    course_title = serializers.CharField(source="course.title", read_only=True)
    course_code = serializers.CharField(source="course.code", read_only=True)
    lesson_title= serializers.CharField(source= "lesson.title", read_only= True)
    lesson_code= serializers.CharField(source= "lesson.code", read_only= True)
    enrolled_count = serializers.ReadOnlyField()
    available_spot = serializers.ReadOnlyField()
    
    class Meta:
        model = Class
        fields = ["id","title", "semester","teacher_name","course_title","lessson_title", "lesson_code", 
                 "course_code","capacity", "enrolled_count", "available_spot", "is_active"]
    
    def create (self,validated_data):
        class_list= Class.objects.create (
            teacher_name= validated_data.pop("teacher_name"),
            course_title=validated_data.pop ("course_title"),
            course_code= validated_data.pop ("course_code"),
            lesson_title= validated_data.pop ("lesson_title"),
            lesson_code= validated_data.pop ("lesson_code"),
            enrolled_count= validated_data.pop ("enrolled_count"),
            available_spot= validated_data.pop ("available_spot"),**validated_data
        )
        return class_list


class EnrollmentSerializer (serializers.ModelSerializer):
    student= StudentSerializer (read_only=True)
    class_instance = ClassSerializer (read_only=True)
    student_id= serializers.CharField(write_only=True, required=False)
    class_id = serializers.CharField(write_only=True)
    available_spot= serializers.ReadOnlyField()
    enrolled_count= serializers.ReadOnlyField()

    class Meta: 
        model= Enrollment
        fields= ["id","student","classes","class_id","is_active","student_id","enrolled_at","capacity","enrolled_count","available_spot"]
        read_only_fields= ["id"]

    def create (self,validated_data):
        student_id= validated_data.pop ("student_id")
        class_id= validated_data.pop ("class_id")
        enrollment= Enrollment.objects.create (student_id= student_id,class_id= class_id,**validated_data)
        return enrollment
    
    def validate(self,data):
        class_instance= Class.objects.get (id=data["class_id"])

        if class_instance.available_spot <= 0 :
            raise serializers.ValidationError("This class is full")
        
        student_id= data.get ("student_id") or self.context ["request"].user.student_profile.id
        if Enrollment.objects.filter(student_id=student_id, classes= class_instance, is_active=True).exists():
            raise serializers.ValidationError ("This students is enrolled")
        return data
        
class AttendanceSerializer (serializers.ModelSerializer):
    # student= StudentSerializer (read_only=True) 
    # lesson= LessonSerializer (many= True, read_only= True)
    # course= CourseSerializer (many= True, read_only= True)
    student_name= serializers.CharField (source="student.user.get_full_name" )
    course_title= serializers.CharField (source= "course.title")
    lesson_title= serializers.CharField (source="lesson.title")

    class Meta:
        model = Attendance
        fields= ["id","student","lesson","course","recorded_at","note","status","student_name","course_title","lesson_title"]
        read_only_fields= ["id"]

    def create (self,validated_data):
        student_name= validated_data.pop ("student_name")
        course_title= validated_data.pop ("course_title")
        lesson_type= validated_data.pop ("lesson_type")
        attendance= Attendance.objects.create (
            student_name=student_name,
            course_title=course_title,
            lesson_type=lesson_type,
            **validated_data)
        return attendance