
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Lesson, Homework, HomeworkGrade,HomeworkSubmission
from .serializers import (LessonSerializer, HomeworkSerializer, 
                          HomeworkGradeSerializer,HomeworkCreateSerializer,
                          HomeworkSubmissionSerializer)

class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Darslarni yaratish va ko'rish"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != "teacher":
            raise PermissionDenied("Faqat o'qituvchilar dars yaratishi mumkin")
        serializer.save(teacher=self.request.user)

class LessonDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        lesson = self.get_object()
        if self.request.user.role != "teacher" or self.request.user != lesson.teacher:
            raise PermissionDenied("Faqat o'z darslaringizni tahrirlashingiz mumkin")
        serializer.save()
    
    def perform_destroy(self, instance):
        if self.request.user.role != "teacher" or self.request.user != instance.teacher:
            raise PermissionDenied("Faqat o'z darslaringizni o'chira olasiz")
        instance.delete()

class HomeworkCreateAPIView(generics.CreateAPIView):
    queryset = Homework.objects.all()
    serializer_class = HomeworkCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user

        if user.role != "teacher":
            raise PermissionDenied("Faqat o'qituvchilar uy vazifasini yaratishi mumkin")
        
        serializer.save(student=user)

class HomeworkListCreateAPIView(generics.ListCreateAPIView):
    """O'quvchi uyga vazifa yuklashi"""
    queryset = HomeworkSubmission.objects.all()
    serializer_class = HomeworkSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        homework = serializer.validated_data["homework"] 
        lesson = homework.lesson 
     
        if user.role != "student":
            raise PermissionDenied("Faqat talabalar vazifa yuklashi mumkin")

        
        if lesson.group not in user.groups.all():  
            raise PermissionDenied("Siz bu dars uchun vazifa yuklay olmaysiz")

        serializer.save(student=user)


class HomeworkDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self,serializer):
        homework = self.get_object()
        if self.request.user.role != "student" or self.request.user != homework.student:
            raise PermissionDenied("Faqat o'z uyga vazifangizni tahrirlashingiz mumkin")
        if not homework.is_editable():
            raise PermissionDenied("Vazifa topshirish muddati tugagan!!!")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role != "student" or self.request.user != instance.student:
            raise PermissionDenied("Faqat o'z uyga vazifangizni o'chira olasiz")
        if not instance.is_editable():
            raise PermissionDenied("Vazifa topshirish muddati tugagan o'chirish mumkin emas")
        instance.delete()

class HomeworkGradeCreateAPIView(generics.CreateAPIView):
    
    queryset = HomeworkGrade.objects.all()
    serializer_class = HomeworkGradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        
        homework = serializer.validated_data.get("homework")
        if self.request.user.role != "teacher" or self.request.user != homework.lesson.teacher:
            raise PermissionDenied("Faqat o‘z darslaringizdagi vazifalarni baholashingiz mumkin")
        if homework.is_editable():
            raise PermissionDenied("Vazifa topshirish muddati hali tugamagan!!!")
        serializer.save(teacher=self.request.user)