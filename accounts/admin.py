from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin 
from django.utils.translation import gettext_lazy as _
from .models import UserModel
from students.models import StudentModel
from teachers.models import TeacherModel
from parents.models import ParentsModel

class StudentInLine (admin.StackedInline):
    model= StudentModel
    extra = 0

class TeacherInLine (admin.StackedInline):
    model = TeacherModel
    extra = 0

class ParentInLine (admin.StackedInline):
    model = ParentsModel
    extra = 0

@admin.register (UserModel)
class UserInLine (DjangoUserAdmin):
    search_fields= ("national_id_number","role","email","username","first_name","last_name")
    list_display = ("id","username","role","date_of_birth","is_staff","is_superuser")
    list_filter = ("role","date_of_birth","is_staff","is_active","is_superuser")
    ordering = ("id",)
    inlines = [StudentInLine, TeacherInLine, ParentInLine]

    fieldsets= (
        (None, {"fields":("username","password")}),
        (_ ("Personal info"), {"fields": ("first_name","last_name","email","national_id_number")}),
        (_ ("Role"), {"fields":("role",)}),
        (_ ("Permissions"), {"fields":("is_active","is_staff","is_superuser")}),
        (_ ("Important_date"),{"fields":("updated_at","created_at")})
                  )

    add_fieldsets=  (
        (None, {"classes":("wide",),
            "fields": ("username","password1","password2","role","email","first_name","last_name")
            }),
                    )