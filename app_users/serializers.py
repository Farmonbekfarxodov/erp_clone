from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "id_number","password", "role","phone_number", "gender")
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
                user.is_staff = True

            user.save()
        return user

    def update(self,instance,validated_data):
        password = validated_data.pop("password",None)
        if password:
            instance.set_password(password)
            instance.save()
        return super().update(instance,validated_data)