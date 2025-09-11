from .models import UserModel
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class UserModelSerializer (serializers.ModelSerializer):
     password = serializers.CharField  (write_only= True)
     class Meta:
        model= UserModel
        fields = ["id","username","password","first_name","last_name","email","role","gender","date_of_birth","created_at","updated_at","phone","adress","national_id_number","province","city"] 
        read_only_field = ["id","created_at","updated_at"]
        
        def create (self,validated_data):
            password = validated_data.pop ("password")
            user = UserModel.objects.create (
            username=validated_data ["username"],
            email= validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            role=validated_data["role"],
            gender= validated_data ["gender"],
            date_of_birth= validated_data ["date_of_birth"],
            phone=validated_data ["phone"],
            adress= validated_data["adress"],
            national_id_number= validated_data["national_id_number"],
            province= validated_data ["province"], 
            city= validated_data ["city"]


              )
            validate_password(password,user)
            user.set_password (password)
            user.save()
            return user
        
        def update(self, instance, validated_data):
           password = validated_data.pop ("password",None)
           for key,value in validate_password.items():
            setattr (instance,key,value)
            if password:
             validate_password(instance,password)
            instance.set_password (password)
            instance.save ()
            return instance

