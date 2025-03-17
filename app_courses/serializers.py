
from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

    def create(self,validated_data):
        validated_data["admin"] = self.context["request"].user
        return super().create(validated_data)