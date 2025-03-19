from datetime import timedelta
from rest_framework import serializers
from django.utils.timezone import now
from datetime import datetime


from .models import  HomeworkSubmission, Lesson, Homework

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class HomeworkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ["description","deadline","lesson"]
    
    def validate(self,data):
        request = self.context["request"]
        lesson = data["lesson"]

        if request.user.role != "teacher":
            raise serializers.ValidationError("Faqat o'qituvchilar uy vazifasini yaratishlari mumkin")
        
        if lesson.teacher != request.user:
            raise serializers.ValidationError("Siz faqat o'z darslaringiz uchun vazifa yaratishingiz mumkin")

        return data
      
class HomeworkSerializer(serializers.ModelSerializer):
    deadline = serializers.CharField()

    class Meta:
        model = Homework
        fields = "__all__"
        read_only_fields = ["student","submitted_at"]
    
    def validate_lesson(self,value):
        user = self.context["request"].user
        if user.role != "student":
            raise serializers.ValidationError("Faqat talabalar vazifa yuklay olishi mumkin")
        if value.group not in user.groups.all():
            raise serializers.ValidationError("Siz bu darsga vazifa yuklay olmaysiz")
        return value
    
    def create(self,validated_data):
        validated_data["student"] = self.context["request"].user
        return super().create(validated_data)
    
    def validate_deadline(self,value):
        try:
            hours = int(value)
            return now() + timedelta(hours=hours)
        except ValueError:
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                raise serializers.ValidationError("vaqtni kiriting")
            

class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    """Talaba yuklagan uyga vazifa serializeri"""
    

    class Meta:
        model = HomeworkSubmission
        fields = ["id", "homework", "student", "file", "text", "comment", "submitted_at", "grade"]
        read_only_fields = ["student", "submitted_at"]




class HomeworkGradingSerializer(serializers.ModelSerializer):
    """O'qituvchi uy vazifalarini baholashi uchun serializer"""
    
    class Meta:
        model = HomeworkSubmission
        fields = ["grade"]  