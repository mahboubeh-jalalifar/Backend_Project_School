from django.contrib import admin
from .models import TeacherModel

@admin.register (TeacherModel)
class TeacherAdmin (admin.ModelAdmin):
    search_fields=("user__username", "user__email", "department")
    list_display= ("id", "user", "department")
    raw_id_fields= ("user",)
