from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import generics,permissions
# from rest_framework.permissions import AllowAny


from .models import CustomUser
from .serializers import (CreateUserSerializer,)

# class RegisterView(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = RegisterSerializer
#     permission_classes = [AllowAny]

class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [permissions.IsAdminUser]

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


    