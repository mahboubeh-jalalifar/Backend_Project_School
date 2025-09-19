from django.db import models
from django.conf import settings

class StudentModel (models.Model):
    user= models.OneToOneField (settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name="student_profile")
    grade= models.DateTimeField ()
    major=models.CharField (max_length=30)
    GPA= models.DecimalField(max_digits=4, decimal_places=2)
    enrollment_date= models.DateTimeField ()
    is_active= models.BooleanField (default=True)
    bio= models.TextField (max_length=500, blank=True)
    
    def __str__ (self):
            return f"The name of the student is {self.user.username} sudying in {self.major} with GPA {self.GPA}."
            

