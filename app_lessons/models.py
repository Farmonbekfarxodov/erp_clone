from django.db import models
from app_users.models import CustomUser
from app_groups.models import Groups

class Lesson(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name="lesson_groups")
    teacher = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="lesson_teachers")
    topic = models.CharField(max_length=255)
    content = models.TextField()
    video = models.FileField(upload_to="lesson_videos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.group.name} - {self.topic}"

class Homework(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="homework_lesson")
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="homework_student")
    file = models.FileField(upload_to="homeworks/", blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vazifa: {self.lesson.topic} - {self.student.username}"

class HomeworkGrade(models.Model):
    homework = models.OneToOneField(Homework, on_delete=models.CASCADE, related_name="homework_grade")  # related_name o'zgartirildi
    teacher = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="graded_homework")
    score = models.IntegerField()
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.homework.student.username} - {self.homework.lesson.topic}"
