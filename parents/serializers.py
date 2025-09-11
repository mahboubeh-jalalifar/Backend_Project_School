from rest_framework import serializers
from .models import ParentsModel

class ParentsSerializer (serializers.ModelSerializer):
    class Meta:
        model= ParentsModel
        fields= ["id","user","type_of_family_relation","children"]
        read_only_field= ["id"]
        def create (self,validated_data):
            user= ParentsModel.objects.all (**validated_data)
            return user