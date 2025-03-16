from django.contrib import admin
from app_lessons.models import Lesson, Homework

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "group", "teacher", "topic", "created_at")
    list_filter = ("group", "teacher")
    search_fields = ("topic", "content")
    ordering = ("-created_at",)

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ("id", "lesson", "student", "grade")
    list_filter = ("lesson", "student", "grade")
    search_fields = ("lesson__topic", "student__username")
    ordering = ("lesson", "student")
