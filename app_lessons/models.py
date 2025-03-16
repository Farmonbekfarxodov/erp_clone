
from django.db import models
from app_users.models import CustomUser
from app_groups.models import Groups

class Lesson(models.Model):
    group = models.ForeignKey(Groups,on_delete=models.CASCADE,
                              related_name="lesson_groups")
    teacher = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,
                                null=True,blank=True,
                                related_name="lesson_teachers")
    topic = models.CharField(max_length=255)
    content = models.TextField()
    video = models.FileField(upload_to="lesson_videos/",blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.group.name}-{self.topic}"

class Homework(models.Model):
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,
                               related_name="homework_lesson")
    student = models.ForeignKey(CustomUser,on_delete=models.CASCADE,
                                related_name="homewrok_student")
    file = models.FileField(upload_to="homeworks/",blank=True,null=True)
    grade = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f"Vazifa {self.lesson.topic} ga {self.student.username}"
    