from django.db import models
from app_users.models import CustomUser
from app_groups.models import Groups


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    admin = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,  
        null=True, 
        blank=True, 
        related_name="created_courses"  
    )
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,blank=True,
        related_name="teaching_courses"
    )

    groups = models.ManyToManyField(Groups, related_name="courses", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title