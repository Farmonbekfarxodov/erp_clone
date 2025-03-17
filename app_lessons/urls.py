from django.urls import path
from .views import (
    LessonListCreateAPIView, LessonDetailAPIView,
    HomeworkListCreateAPIView, HomeworkDetailAPIView
)

app_name = "lessons"

urlpatterns = [
    # 📌 Darslar (Lessons)
    path("lessons/", LessonListCreateAPIView.as_view(), name="lesson-list-create"),  # Dars yaratish va ko'rish
    path("lessons/<int:pk>/", LessonDetailAPIView.as_view(), name="lesson-detail"),  # Bitta darsni ko'rish, yangilash, o'chirish

    # 📌 Uy vazifalari (Homeworks)
    path("homeworks/", HomeworkListCreateAPIView.as_view(), name="homework-list-create"),  # Uy vazifalarini yaratish va ko'rish
    path("homeworks/<int:pk>/", HomeworkDetailAPIView.as_view(), name="homework-detail"),  # Uy vazifasini ko'rish va baholash
]
