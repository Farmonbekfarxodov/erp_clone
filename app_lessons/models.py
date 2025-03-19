
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now


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
    """O'qituvchi tomonidan berilgan uyga vazifa"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    description = models.TextField()
    deadline = models.DateTimeField()

    def is_editable(self):
        """Vazifa topshirish muddati tugagan yoki yo‘qligini tekshirish"""
        return now() < self.deadline    

class HomeworkSubmission(models.Model):
    """Talaba tomonidan yuklangan uy vazifasi"""
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="homework_submissions/", blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)  # ✅ Qo'shish kerak bo'lsa!
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.PositiveIntegerField(blank=True, null=True) 
    
class HomeworkGrade(models.Model):
    """O'qituvchi tomonidan qo‘yilgan baho"""
    homework_submission = models.OneToOneField(
        HomeworkSubmission, on_delete=models.CASCADE, related_name="homework_grade"
    )
    teacher = models.ForeignKey(
       User, on_delete=models.SET_NULL, null=True, blank=True, related_name="graded_homework"
    )
    score = models.PositiveIntegerField() 
    feedback = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.homework_submission.student.username} - {self.homework_submission.homework.lesson.topic}"