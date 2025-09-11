from django.contrib import admin
from .models import ParentsModel

@admin.register(ParentsModel)
class ParentAdmin (admin.ModelAdmin):
    list_display=("user","type_of_family_relation")
    search_fields= ("user","user__username", "user__email")
    raw_id_fields= ("user",)
