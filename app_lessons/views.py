from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from drf_yasg.utils import swagger_auto_schema

from .models import Lesson, Homework
from .serializers import LessonSerializer, HomeworkSerializer

class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Guruhga bog'langan darslarni ko'rish va yaratish"""
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Foydalanuvchi faqat o'ziga tegishli guruhlarning darslarini ko'rishi kerak"""
        user = self.request.user
        if user.role == "teacher":
            return Lesson.objects.filter(group__in=user.groups.all())
        elif user.role == "student":
            return Lesson.objects.filter(group__students=user)
        return Lesson.objects.none()

    def perform_create(self, serializer):
        """O'qituvchi faqat o'ziga tegishli guruhlar uchun dars yaratadi"""
        user = self.request.user
        if user.role != "teacher":
            raise PermissionDenied("Faqat o'qituvchilar dars yaratishi mumkin")
        
        group = serializer.validated_data["group"]
        if group not in user.groups.all():
            raise PermissionDenied("Siz faqat o'z guruhlaringiz uchun dars yaratishingiz mumkin")
        
        serializer.save(teacher=user)

class LessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Bitta darsni olish, yangilash yoki o'chirish"""
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(auto_schema=None)  # Swagger uchun schema generatsiyasini o‘chirib qo‘yamiz
    def get_queryset(self):
        """Faqat autentifikatsiyadan o'tgan foydalanuvchilar o‘z guruhlarining darslarini ko‘ra oladi"""
        user = self.request.user

        if not user.is_authenticated:
            return Lesson.objects.none()

        if user.role == "teacher":
            return Lesson.objects.filter(teacher=user)
        elif user.role == "student":
            return Lesson.objects.filter(group__students=user)

        return Lesson.objects.none()

class HomeworkListCreateAPIView(generics.ListCreateAPIView):
    """Uy vazifasi yaratish va ro'yxatini ko'rish"""
    serializer_class = HomeworkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Foydalanuvchi faqat o‘z guruhidagi darslar uchun uy vazifalarini ko‘rishi kerak"""
        user = self.request.user
        if user.role == "student":
            return Homework.objects.filter(student=user)
        elif user.role == "teacher":
            return Homework.objects.filter(lesson__group__in=user.groups.all())
        return Homework.objects.none()

    def perform_create(self, serializer):
        """Faqat o'quvchilar o'z guruhlaridagi darslar uchun vazifa topshira oladi"""
        user = self.request.user
        if user.role != "student":
            raise PermissionDenied("Faqat talabalar vazifa yuklashlari mumkin")
        
        lesson = serializer.validated_data["lesson"]
        if lesson.group not in user.groups.all():
            raise PermissionDenied("Siz faqat o'z guruhingiz uchun vazifa yuklashingiz mumkin")

        serializer.save(student=user)

class HomeworkDetailAPIView(generics.RetrieveUpdateAPIView):
    """Uy vazifalarini ko'rish va baholash"""
    serializer_class = HomeworkSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(auto_schema=None)  # Swagger uchun schema generatsiyasini o‘chirib qo‘yamiz
    def get_queryset(self):
        """Faqat autentifikatsiyadan o'tgan foydalanuvchilar o‘z guruhlarining uy vazifalarini ko‘ra oladi"""
        user = self.request.user

        if not user.is_authenticated:
            return Homework.objects.none()  

        if user.role == "teacher":
            return Homework.objects.filter(lesson__group__in=user.groups.all())
        elif user.role == "student":
            return Homework.objects.filter(student=user)

        return Homework.objects.none()
    
    def perform_update(self, serializer):
        """Faqat o'qituvchi o'z guruhidagi talabalar uchun baho qo'ya oladi"""
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied("Foydalanuvchi autentifikatsiyadan o'tmagan")

        if user.role != "teacher":
            raise PermissionDenied("Faqat o'qituvchilar uy vazifasini baholay oladi")

        homework = self.get_object()
        if homework.lesson.group not in user.groups.all():
            raise PermissionDenied("Siz faqat o‘z guruhingizdagi talabalar uchun baho qo'ya olasiz")

        serializer.save()

