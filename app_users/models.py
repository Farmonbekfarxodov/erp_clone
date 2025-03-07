from django.contrib.auth.models import AbstractUser
from django.db import models

class UserRoles(models.TextChoices):

    SUPERADMIN  = "superadmin", "Superadmin"
    ADMIN = "admin", "Admin"
    TEACHER = "teacher", "Teacher"
    STUDENT = "student", "Student"

class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRoles.choices,
        default=UserRoles.STUDENT
    )
    profile_picture = models.ImageField(upload_to="profiles/",null=True,blank=True)

    def __str__(self):
        return self.username