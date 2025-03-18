from django.contrib import admin
from .models import Lesson, Homework, HomeworkGrade

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id","topic", "group", "teacher", "created_at")
    list_filter = ("group", "teacher")
    search_fields = ("topic", "teacher__username")

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ("id","lesson", "student", "submitted_at")  
    search_fields = ("lesson__topic", "student__username")

@admin.register(HomeworkGrade)
class HomeworkGradeAdmin(admin.ModelAdmin):
    list_display = ("homework", "teacher", "score", "created_at")
    list_filter = ("score", "teacher")
    search_fields = ("homework__lesson__topic", "teacher__username")
