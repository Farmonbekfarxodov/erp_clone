from django.urls import path
from .views import (CourseListCreateAPIView,CourseDetailAPIView)

app_name = "courses"

urlpatterns = [
    path("courses/",CourseListCreateAPIView.as_view(),name="course-list-create"),
    path("courses/<int:pk>/",CourseDetailAPIView.as_view(),name="couse-detail"),
]