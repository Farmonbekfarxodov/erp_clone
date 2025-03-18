
from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "description", "teacher", "groups", "created_at"]
        read_only_fields = ["created_at"]

    def create(self,validated_data):
        validated_data["admin"] = self.context["request"].user
        return super().create(validated_data)