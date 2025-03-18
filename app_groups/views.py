from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from app_groups.models import Groups
from app_groups.serializers import GroupSerializer

class IsAdminPermission(IsAuthenticated):
    """Faqat adminlarga ruxsat berish"""
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role =="admin"

class GroupListCreateAPIView(generics.ListCreateAPIView):
    """Guruhlar ro'yxati va yangi guruh yaratish"""
    queryset = Groups.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminPermission()]
        return [IsAuthenticated()]

    def perform_create(self,serializer):
        """Admin bo'lmasa guruh yarata olmaydi"""
        if self.request.user.role != "admin":
            raise PermissionDenied("Faqat adminlar guruh yarata olishi mumkin")
        serializer.save()

class GroupDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Bitta guruhni olish , yangilash , o'chirish"""
    queryset = Groups.objects.all()
    serializer_class = GroupSerializer

    def get_permissions(self):
        if self.request.method in ["PUT","DELETE"]:
            return [IsAdminPermission()]
        return [IsAuthenticated()]