from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date


class Roles (models.TextChoices):
       Admin= "Admin","Admin",
       Employee= "Employee","Employee",
       Teacher=  "Teacher","Teacher",
       Student= "Student","Student",
       Parents= "Parents","Parents",
       Others= "Others","Others",

class Gender (models.TextChoices):
     Male= "Male","Male",
     Female= "Female","female",
     Other= "Other","Other",
                   
class UserModel (AbstractUser):
    role= models.CharField (max_length=50 , choices=Roles.choices , default=Roles.Student)
    email= models.EmailField (max_length=200, unique=True )
    national_id_number= models.CharField (unique=True, null= True , blank=True)
    phone=models.CharField (blank=True,null=True)
    address=models.CharField(max_length=200,blank=True,null=True)
    city= models.CharField(max_length=30)
    province= models.CharField(max_length=30)
    date_of_birth= models.DateField (blank=True,null=True)
    gender= models.CharField (max_length=30,choices=Gender.choices, null=True,blank=True)
    updated_at= models.DateTimeField (auto_now=True)
    created_at=models.DateTimeField (auto_now_add=True)
    def __str__(self):
        return f"{self.username} is {self.role}"

    



    



