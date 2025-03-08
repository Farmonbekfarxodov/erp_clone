from django.contrib.auth import get_user_model
from rest_framework import serializers




# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ("id","username","email","password","role")
        
#     def create(self,validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user


User = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "password", "role", "id_number", "phone_number", "gender")
        extra_kwargs = {
            "password":{"write_only":True,"required":False},
            "email":{"required":False}
        }

    def create(self, validated_data):
        role = validated_data.pop("role", None)  # Role ni ajratib olish
        user = User.objects.create_user(**validated_data)  # User yaratish
        if role:
            user.role = role  # Role ni 
            if user.role == 'admin': 
                user.is_staff = True
                user.is_superuser = True

            user.save()
        return user

    def update(self,instance,validated_data):
        password = validated_data.pop("password",None)
        if password:
            instance.set_password(password)
        return super().update(instance,validated_data)