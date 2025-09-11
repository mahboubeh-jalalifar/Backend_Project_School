from rest_framework import serializers 
from .models import TeacherModel
class TeacherSerializer (serializers.ModelSerializer):
    class Meta:
        model = TeacherModel
        fields= ["id","user", "deparment", "subjects" , "education_level", "hire_date", "bio"]
        read_only_field= ["id"]

        def create (self,validated_data):
            user = TeacherModel.objects.all (**validated_data)
            return user 