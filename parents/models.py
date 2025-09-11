from django.db import models
from django.conf import settings

class Relation (models.TextChoices):
    Father= "Father","Father"
    Mother= "Mother","Mother"
    Others= "Others","Others"

class Children (models.Model):
    name= models.CharField (max_length=50)
    def __str__(self):
        return self.name

class ParentsModel (models.Model):
    user= models.OneToOneField (settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type_of_family_relation= models.CharField (choices=Relation.choices)
    children = models.ManyToManyField (Children, related_name="parent_of_children")
    def __str__ (self):
        return self.user
