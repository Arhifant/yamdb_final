from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TokenObtainAPIView, UserSignupAPIView,  # isort:skip
                    UserViewSet)

v1_router = DefaultRouter()
v1_router.register(r"users", UserViewSet)


app_name = "users"

urlpatterns = [
    path("v1/auth/signup/", UserSignupAPIView.as_view(), name="signup"),
    path("v1/auth/token/", TokenObtainAPIView.as_view(), name="obtain_token"),
    path("v1/", include(v1_router.urls)),
]
