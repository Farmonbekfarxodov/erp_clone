from django.urls import path
from .views import (
    LessonListCreateAPIView, LessonDetailAPIView,
    HomeworkListCreateAPIView, HomeworkDetailAPIView,HomeworkCreateAPIView,
)

app_name = "lessons"

urlpatterns = [
 
    path("lessons/", LessonListCreateAPIView.as_view(), name="lesson-list-create"),   
    path("lessons/<int:pk>/", LessonDetailAPIView.as_view(), name="lesson-detail"),  
    path("homeworks/", HomeworkListCreateAPIView.as_view(), name="homework-list-create"), 
    path("homeworks/create/", HomeworkCreateAPIView.as_view(),name="homework-create"),
    path("homeworks/<int:pk>/", HomeworkDetailAPIView.as_view(), name="homework-detail"),  
]
