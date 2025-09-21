from django.contrib import admin
from .models import Lesson, Course, Class, Attendance, Enrollment

@admin.register (Lesson)
class LessonAdmin (admin.ModelAdmin):
    search_fields=("code","title")
    list_display= ("id","code","title","start_date","prerequisites","credits","schedule","duration","lesson_type")
    list_filter= ("code","title")
    date_hierarchy= "start_date"

@admin.register (Course)
class CourseAdmin (admin.ModelAdmin):
    search_fields=("code","title")
    list_display= ("id","code","title","start_date","prerequisites","credits","lesson_type","price")
    date_hierarchy= "start_date"
    list_filter= ("price",)

@admin.register (Class)
class ClassAdmin (admin.ModelAdmin):
    search_fields=("name","course")
    list_display= ("id","name","course","teacher","room_number","building","is_active","capacity")
    raw_id_fields = ("course","teacher")
    list_filter  = ("room_number","is_active")
    readonly_fields= ("id",)


@admin.register (Enrollment)
class EnrollmentsAdmin (admin.ModelAdmin):
    list_display=("id","student__user__username","class_instance","enrolled_at","is_active")
    search_fields= ("student__user__username","class_instance__name")
    date_hierarchy= "enrolled_at"
    list_filter= ("enrolled_at",)
    raw_id_fields = ("student","class_instance")

admin.register (Attendance)
class AttendanceAdmin (admin.ModelAdmin):
    list_display= ("id","student__user__username","class_instance__name","lesson","student""status","recorded_at")
    search_fields= ("id","student__user__username","class_instance__name","lesson__title","course__title")
    list_filter= ("status",)
    raw_id_filds = ("leesson","student")
    date_hierarchy = "recorded_at"