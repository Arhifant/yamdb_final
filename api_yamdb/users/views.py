from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdmin
from .serializers import (UserSerializer, UserSignupSerializer,
                          UserTokenObtainingSerializer)
from .utils import send_confirmation_code

User = get_user_model()


class UserSignupAPIView(APIView):
    """
    Obtaining confirmation code (possibly with registration at the same time)
    by user.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user, created = User.objects.get_or_create(**serializer.data)
        except IntegrityError:
            return Response(
                serializer.data, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            if created:
                user.set_unusable_password()  # type:ignore
                user.save()

        send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainAPIView(APIView):
    """
    Obtaining authorization token with email and confirmation_code provided.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserTokenObtainingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        confirmation_code = serializer.validated_data.get("confirmation_code")

        if not User.objects.filter(username=username).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not User.objects.filter(
            confirmation_code=confirmation_code
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(
            User,
            username=username,
            confirmation_code=confirmation_code
        )
        refresh_token = RefreshToken.for_user(user)
        resp = {
            "token": str(refresh_token.access_token)
        }
        return Response(
            resp, status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    """
    User viewset.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    permission_classes = (IsAdmin,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.pk == instance.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=["get", "patch"],
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer_class = self.get_serializer_class()
        if request.method == "PATCH":
            serializer = serializer_class(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.validated_data.pop("role", None)
            serializer.save()
        serializer = serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
