from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
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
    profile_picture = models.ImageField(upload_to="profiles/",
                                        null=True,blank=True)
    id_number = models.CharField(max_length=20,unique=True,
                                 null=True,blank=True)
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    gender = models.CharField(max_length=10,choices=[("male","Male"),("female","Female")],
                              null=True,blank=True)
    
  
    def __str__(self):
        return self.username


    
User = get_user_model()
