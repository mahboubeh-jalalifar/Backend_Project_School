from rest_framework import serializers
from .models import ParentsModel

class ParentsSerializer (serializers.ModelSerializer):
    class Meta:
        model= ParentsModel
        fields= ["id","user","type_of_family_relation","children"]
        read_only_fields= ["id"]
        
    # def create (self,validated_data):
    #     user= validated_data.pop ("user")
    #     parent= ParentsModel.objects.create (user=user,**validated_data)
    #     return parent