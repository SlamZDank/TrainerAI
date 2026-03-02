from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()

ACCESS_MAX_AGE = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
REFRESH_MAX_AGE = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())

COOKIE_DEFAULTS = {
    "httponly": True,
    "secure": not settings.DEBUG,
    "samesite": "Lax",
}


def _set_tokens(response, user):
    refresh = RefreshToken.for_user(user)
    response.set_cookie("access_token", str(refresh.access_token), max_age=ACCESS_MAX_AGE, **COOKIE_DEFAULTS)
    response.set_cookie("refresh_token", str(refresh), max_age=REFRESH_MAX_AGE, **COOKIE_DEFAULTS)


def _clear_tokens(response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            # 409 for duplicate email, 400 for everything else
            if "email" in serializer.errors and any(
                "already exists" in str(e) for e in serializer.errors["email"]
            ):
                return Response({"errors": serializer.errors}, status=status.HTTP_409_CONFLICT)
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        response = Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        _set_tokens(response, user)
        return response


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response(
                {"errors": {"detail": "Invalid email or password."}},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        response = Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        _set_tokens(response, user)
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        _clear_tokens(response)
        return response


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        raw_refresh = request.COOKIES.get("refresh_token")
        if not raw_refresh:
            return Response(
                {"errors": {"detail": "Token is invalid or expired."}},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            refresh = RefreshToken(raw_refresh)
            access_token = str(refresh.access_token)
        except TokenError:
            return Response(
                {"errors": {"detail": "Token is invalid or expired."}},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        response = Response({"detail": "Token refreshed."}, status=status.HTTP_200_OK)
        response.set_cookie("access_token", access_token, max_age=ACCESS_MAX_AGE, **COOKIE_DEFAULTS)
        return response


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
