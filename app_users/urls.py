from django.urls import path
from app_users import views
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

app_name = "users"

urlpatterns = [
    path("login/",TokenObtainPairView.as_view(),name="login"),
    path("token/refresh/",TokenRefreshView.as_view(),name="token_refresh"),
    #path("create/",views.CreateUserView.as_view(),name="create"),
    path("profile/",views.UserUpdateView.as_view(),name="user-profile"),
    path("users/",views.UserListCreateAPIView.as_view(),name="users"),
    path("users/<int:pk>/",views.UserDetailAPIView.as_view(),name="user-detail"),
]
