from django.urls import path
from .views import (
    LessonListCreateAPIView, LessonDetailAPIView,
    HomeworkSubmissionListCreateAPIView,HomeworkGradingAPIView,
    HomeworkCreateAPIView,HomeworkDetailAPIView
)

app_name = "lessons"

urlpatterns = [
 
    path("lessons/", LessonListCreateAPIView.as_view(), name="lesson-list-create"),   
    path("lessons/<int:pk>/", LessonDetailAPIView.as_view(), name="lesson-detail"),  
    path("homeworks/create/", HomeworkCreateAPIView.as_view(),name="homework-create"),
    path("homeworks/submissions/", HomeworkSubmissionListCreateAPIView.as_view(), name="homework_submissions"),
    path("homeworks/submissions/<int:pk>/grade/", HomeworkGradingAPIView.as_view(), name="homework_grading"),
    path("homeworks/<int:pk>/", HomeworkDetailAPIView.as_view(), name="homework-detail"),  
    
]
