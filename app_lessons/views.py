from rest_framework import generics,permissions
from rest_framework.exceptions import PermissionDenied
from .models import Lesson,Homework
from .serializers import LessonSerializer,HomeworkSerializer

class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Guruhga bog'langan darslarni ko'rish va yaratish"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """O'qituvchi faqat o'ziga tegishli guruhlar uchun dars yaratadi"""
        user = self.request.user
        if user.role != "teacher":
            raise PermissionDenied("Faqat o'qituvchilar dars yaratishi mumkin")
        serializer.save()

class LessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Bitta darsni olish yangilash yoki o'chirish"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

class HomeworkListCreateAPIView(generics.ListCreateAPIView):
    """Uy vazifasi yaratish va ro'yxatini ko'rish"""
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Faqat o'quvchilar vazifa topshira oladi"""
        user = self.request.user
        if user.role != "student":
            raise PermissionDenied("Faqat talabalar vazifa yuklashlari mumkin")
        serializer.save(student=user)

class HomeworkDetailAPIView(generics.RetrieveUpdateAPIView):
    """Uy vazifalarini ko'rish baholash"""
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self,serializer):
        """Faqat o'quvchi uy vazifasini bajara oladi"""
        user = self.request.user
        if user.role != "teacher":
            raise PermissionDenied("Faqat o'qituvchilar uy vazifasini baolay oladi")
        serializer.save()
        