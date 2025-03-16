
from rest_framework import serializers
from .models import Lesson, Homework

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
    
class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = "__all__"