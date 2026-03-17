from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from trainerai.apps.user.services import create_user_profile
from .serializers import UserProfileSerializer


class ProfileCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, "profile"):
            return Response({"errors": {"detail": "Profile not found."}}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserProfileSerializer(request.user.profile).data)

    def post(self, request):
        if hasattr(request.user, "profile"):
            return Response(
                {"errors": {"detail": "Profile already exists. Use PATCH to update."}},
                status=status.HTTP_409_CONFLICT,
            )

        serializer = UserProfileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        profile = create_user_profile(
            user=request.user,
            validated_data={
                **serializer.validated_data,
                "disclaimer_accepted_at": timezone.now(),
            },
        )
        return Response(UserProfileSerializer(profile).data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        if not hasattr(request.user, "profile"):
            return Response({"errors": {"detail": "Profile not found."}}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(request.user.profile, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)
