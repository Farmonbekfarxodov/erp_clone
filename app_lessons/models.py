
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from app_users.models import CustomUser
from app_groups.models import Groups

User = get_user_model()

class Lesson(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name="lesson_groups")
    teacher = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="lesson_teachers")
    topic = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)  
    video = models.FileField(upload_to="lesson_videos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.group.name} - {self.topic}"

class Homework(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="homework_lesson")
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="homework_student")
    file = models.FileField(upload_to="homeworks/", blank=True, null=True)
    text = models.TextField(blank=True, null=True) 
    deadline = models.DateTimeField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def is_editable(self):
        return timezone.now() < self.deadline

    def __str__(self):
        return f"Vazifa: {self.lesson.topic} - {self.student.username}"

class HomeworkSubmission(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE,related_name="student_submissions")
    homework = models.ForeignKey(Homework,on_delete=models.CASCADE,related_name="submit_homework")
    file = models.FileField(upload_to="homework_submissions/",blank=True,null=True)
    text = models.TextField(blank=True,null=True)
    comment = models.TextField(blank=True,null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.homework}"

class HomeworkGrade(models.Model):
    homework = models.OneToOneField(Homework, on_delete=models.CASCADE, related_name="homework_grade")
    teacher = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="graded_homework")
    score = models.PositiveIntegerField()  
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.homework.student.username} - {self.homework.lesson.topic}"
