from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "admin")
    search_fields = ("title", "admin__username")
    list_filter = ("admin",)
