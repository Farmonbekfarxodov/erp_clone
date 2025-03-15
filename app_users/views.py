from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics,permissions



from .models import CustomUser
from .serializers import (CreateUserSerializer,)


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
       if self.request.method in ["POST","GET"]:
           return [permissions.IsAdminUser()]
       return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.role == "superadmin":
            return serializer.save()
        elif user.role == "admin":
            role = self.request.data.get("role")
            if role in ["teacher","student"]:
                return serializer.save()
            else:
                raise PermissionDenied("Admin faqat o'qituvchi va student yarata oladi")
        else:
            raise PermissionDenied("Sizda foydalanuvchi yaratish huquqi yo'q")
        
class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self,attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = CustomUser.objects.filter(id_number=username).first() 

        if user and user.check_password(password):
            attrs["username"] = user.username
        return super().validate(attrs)

class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer

class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user #foydalanuvchi faqat o'z profilini o'zgartiradi

class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Bitta foydalanuvchini ko'rish o'chirish va tahrirlash"""
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self,serializer):
        """Faqat adminlar superadminlar foydalanuvchilarni o'zgartira oladi"""
        user =  self.request.user
        if user.role in ["admin","superadmin"]:
            return serializer.save()
        else:
            raise PermissionDenied("Sizda foydalanuvchini o'zgartirish huquqi yo'q")
    
    def perform_destroy(self, instance):
        """Faqat superadmin va adminlar foydalanuvchilarni o'chira oladi"""
        user = self.request.user
        if user.role in ["superadmin","admin"]:
            instance.delete()
        else:
            raise PermissionDenied("Sizda foydalanuvchini o'chirish huquqi yo'q")
    