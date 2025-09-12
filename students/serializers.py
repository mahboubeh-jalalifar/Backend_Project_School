from rest_framework import serializers
from .models import StudentModel

class StudentSerializer (serializers.ModelSerializer):
    class Meta:
        model= StudentModel
        fields= ["id","user","grade","major","GPA","enrollment_date","is_active","bio"]
        read_only_fields= ["id"]
    
    def create (self,validated_data):
        user= validated_data.pop ("user")
        student= StudentModel.objects.create (user=user,**validated_data)
        return student
