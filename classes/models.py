from django.db import models
from django.core.exceptions import ValidationError

class ClassType (models.TextChoices):
    Theory= "Theory","Theory"
    Practical= "Practical","Practical"
    Lecture= "Lecture","Lecture"
    Laboratory= "laboratory","Laboratory"
    Workshop= "Workshop","Workshop"
    Seminar= "Seminar","Seminar"
    Exam= "Exam","Exam"
    Review= "Review","Review"

class Course (models.Model):
    code= models.CharField (max_length=50, unique=True)
    title= models.CharField(max_length=200)
    description= models.TextField ()
    lesson_type= models.CharField (choices=ClassType.choices, default=ClassType.Theory)
    start_date= models.DateField ()
    end_date= models.DateField()
    prerequisites= models.CharField(max_length=50, blank=True)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    discount= models.DecimalField(max_digits=10, decimal_places=2)
    is_free= models.BooleanField (default=True)
    rate= models.IntegerField (default=0)
    credits= models.PositiveIntegerField(default=3)
    score= models.CharField (max_length=5)

    class Meta:
        ordering = ["price","rate"]

    def __str__ (self):
        return f"{self.code}: {self.title}"
    
class Class (models.Model):
    name= models.CharField(max_length=100)
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name="classes")
    teacher= models.ForeignKey("teachers.TeacherModel", on_delete=models.CASCADE, related_name="classes")
    room_number = models.CharField(max_length=20)
    building= models.CharField(max_length=50)
    is_active= models.BooleanField(default=True)
    capacity= models.PositiveIntegerField (default=20)

    class Meta: 
        verbose_name_plural= "classes"
    
    def __str__ (self):
        return f"{self.name}: {self.teacher.user.get_full_name()}"
    
    @property
    def enrolled_count (self):
        return Enrollment.objects.filter(is_active=True).count()

    @property
    def available_spot (self):
        return self.capacity - self.enrolled_count

class Lesson (models.Model):
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='lessons')
    code= models.CharField (max_length=50, unique=True)
    title= models.CharField(max_length=100)
    description= models.TextField()
    start_date= models.DateField ()
    end_date= models.DateField()
    grade= models.CharField (max_length=50)
    prerequisites= models.CharField(max_length=50, blank=True)
    credits= models.PositiveIntegerField(default=3)
    semester= models.CharField(max_length=20)
    schedule= models.DateTimeField ()
    duration= models.PositiveIntegerField(default=45)
    lesson_type= models.CharField(choices=ClassType.choices,default=ClassType.Theory)
    material= models.TextField(help_text="Links for all about things you need", blank= True)
    score= models.CharField (max_length=5)
    def __str__ (self):
        return f"{self.code}: {self.title}"

class Enrollment (models.Model):
    student= models.ForeignKey ("students.StudentModel", on_delete=models.CASCADE, related_name="enrollments")
    class_instance = models.ForeignKey (Class, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateField (auto_now_add=True)
    is_active= models.BooleanField (default=True)

    class Meta:
        unique_together= ["student","class_instance"]

    def __str__ (self):
        return f"{self.student} enrolled in {self.class_instance}"

    def clean (self):
        if self.class_instance.available_spot <= 0 and not self.pk:
            raise ValidationError ("class is full")
    
    def save (self,*args,**kwargs):
        self.clean()
        super().save(*args,**kwargs)


class Status (models.TextChoices):
    Present = "Present", "Present"
    Absent = "Absent","Absent"
    Late = "Late", "Late"
    Excused = "Excused", "Excused"
   
class Attendance (models.Model):
    student= models.ForeignKey("students.StudentModel", on_delete=models.CASCADE, related_name="attendance")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="lesson_attendance")
    course = models.ForeignKey (Course, on_delete= models.CASCADE, related_name="course_attendance")
    recorded_at = models.DateTimeField (auto_now_add=True)
    note = models.CharField (max_length=300, blank=True)
    status = models.CharField (choices= Status.choices, default= Status.Absent)

    class Meta:
        unique_together = ["student","lesson"]
    
    def __str__ (self):
        return f"{self.student} - {self.lesson.title} - {self.note} - {self.status}"




