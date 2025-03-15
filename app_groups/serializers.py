from rest_framework import serializers
from app_groups.models import Groups
from app_users.models import CustomUser


class GroupSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role="teacher"),required=False
    )
    students = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role="student"),many=True,required=False
    )

    class Meta:
        model = Groups
        fields = ["name","teacher","students"]

        def create(self,validated_data):
            request = self.context.get("request")

            if not request or request.user.role != "admin":
                raise serializers.ValidationError("Faqat adminlar guruh yaratishi mumkin")