from django.db import models
from django.conf import settings

class Education (models.TextChoices):
    Bachelor = "Bachelor" , "Bachelor's Degree"
    Master = "Master" , "Master's Degree"
    PhD= "PhD" , "PhD's Degree"
    Postdoctoral = "Postdoctoral" , "Postdoctoral's Degree"

class Subjects (models.Model):
    name= models.CharField (max_length=50)
    def __str__(self) :
        return self.name

class TeacherModel (models.Model):
    user= models.OneToOneField (settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    department= models.CharField (max_length=50)
    subjects= models.ManyToManyField (Subjects, related_name= "Teachers_Subject")
    education_level= models.CharField (choices=Education.choices, default = Education.Bachelor)
    hire_date= models.DateTimeField ()
    bio = models.TextField (max_length=500, blank= True)
    def __str__ (self):
        return self.user.username
