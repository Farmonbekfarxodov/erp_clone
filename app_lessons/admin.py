from django.contrib import admin
from .models import Lesson, Homework, HomeworkGrade,HomeworkSubmission

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "group", "teacher", "created_at")
    list_filter = ("group", "teacher")
    search_fields = ("topic", "teacher__username")

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ("id", "lesson", "description", "deadline")
    list_filter = ("lesson", "deadline")
    search_fields = ("lesson__topic", "description")

@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "homework", "get_student", "submitted_at")
    list_filter = ("homework",)
    search_fields = ("homework__lesson__topic", "student__username")

    @admin.display(description="Student")
    def get_student(self, obj):
        return obj.student.username

@admin.register(HomeworkGrade)
class HomeworkGradeAdmin(admin.ModelAdmin):
    list_display = ("homework_submission", "get_student", "teacher", "score", "created_at")
    list_filter = ("score", "teacher")
    search_fields = ("homework_submission__homework__lesson__topic", "teacher__username")

    @admin.display(description="Student")
    def get_student(self, obj):
        return obj.homework_submission.student.username