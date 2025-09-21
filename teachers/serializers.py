from rest_framework import serializers 
from .models import TeacherModel

class TeacherSerializer (serializers.ModelSerializer):
    class Meta:
        model = TeacherModel
        fields= ["id","user", "department", "subjects" , "education_level", "hire_date", "bio"]
        read_only_fields= ["id"]

    # def create (self,validated_data):
    #     user= validated_data.pop ("user")
    #     teacher = TeacherModel.objects.create (user=user,**validated_data)
    #     return teacher