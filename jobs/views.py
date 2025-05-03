from rest_framework import (
    viewsets,
    permissions,
    generics,
    status,
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Job

from .serializers import JobSerializer
from .serializers_user import UserSignupSerializer

from .permissions import IsEmployer


# Create your views here.
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()    # Defines what data is available
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsEmployer()]
        return [permissions.AllowAny()]


class SignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens for the new user
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
