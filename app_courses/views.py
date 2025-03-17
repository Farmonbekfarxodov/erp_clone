from rest_framework import generics,permissions
from rest_framework.exceptions import PermissionDenied
from .models import Course
from .serializers import CourseSerializer


class CourseListCreateAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self,serializer):
        if self.request.user.role != "admin":
            raise PermissionDenied("Faqat adminlar kurs yarata oladi")
        serializer.save(admin=self.request.user)

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

        