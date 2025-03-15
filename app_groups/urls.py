from django.urls import path
from app_groups.views import GroupListCreateAPIView, GroupDetailAPIView

app_name = "groups"

urlpatterns = [
    path("", GroupListCreateAPIView.as_view(), name="group-list-create"),
    path("groups/<int:pk>/", GroupDetailAPIView.as_view(), name="group-detail"),
]
