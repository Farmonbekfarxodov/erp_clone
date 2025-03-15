from django.db import models
from app_users.models import User

class Groups(models.Model):
    
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="taught_groups"  
    )
    students = models.ManyToManyField(
        User,
        related_name="enrolled_groups", 
        blank=True
    )

    def __str__(self):
        return self.name
    