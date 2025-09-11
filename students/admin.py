from django.contrib import admin
from .models import StudentModel

@admin.register (StudentModel)
class StudentAdmin (admin.ModelAdmin):
    search_fields = ("id","user__username","user__email","user__grade","user__major")
    raw_id_fields = ("user",)
    list_display = ("id","user","grade","major","enrollment_date","GPA")
