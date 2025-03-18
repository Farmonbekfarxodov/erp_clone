from django.contrib import admin
from app_groups.models import Groups

@admin.register(Groups)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id","name", "created_at") 
    search_fields = ("name",)  
    list_filter = ("created_at",)  
    ordering = ("-created_at",)  
