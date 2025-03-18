from rest_framework import generics,permissions
from rest_framework.exceptions import PermissionDenied
from .models import Course
from .serializers import CourseSerializer


class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self,serializer):
       
        user = self.request.user
        if user.role != "admin":
            raise PermissionDenied("Faqat adminlar kurs yarata oladi")
        
        teacher_id = self.request.data.get("teacher")
        if not teacher_id:
            raise PermissionDenied("Kursga o‘qituvchi biriktirish majburiy")

        serializer.save(admin=user)
    
class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self,serializer):
        if self.request.user.role != "admin":
            raise PermissionDenied("Faqat adminlar kurs tahrirlashi mumkin")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role != "admin":
            raise PermissionDenied("Faqat adminlar kursni o'chira oladi")
        instance.delete()

        