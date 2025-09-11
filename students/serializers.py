from rest_framework import serializers
from .models import StudentModel

class StudentSerializer (serializers.ModelSerializer):
    class Meta:
        model= StudentModel
        fields= ["id","user","grade","major","GPA","enrollment_date","is_active","bio"]
        read_only_field = ["id"]
    
    def create (self,validated_data):
        user= StudentModel.objects.all (**validated_data)
        return user
