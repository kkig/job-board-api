from rest_framework import (
    viewsets,
    permissions,
    generics,
    status,
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Job, Application

from .serializers import JobSerializer
from .serializers_user import UserSignupSerializer
from .serializers_application import ApplicationSerializer
from .serializers_applicants import ApplicantSerializer

from .permissions import IsEmployer, IsApplicant


# Create your views here.
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()    # Defines what data is available
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsEmployer()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsApplicant])
    def apply(self, request, pk=None):
        job = self.get_object()
        user = request.user

        # Check for duplicate
        if Application.objects.filter(job=job, applicant=user).exists():
            return Response(
                {"detail": "You have already applied to this job."},
                status=400)

        cover_letter = request.data.get("cover_letter", "")
        application = Application.objects.create(
            job=job,
            applicant=user,
            cover_letter=cover_letter
        )

        serializer = ApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True, methods=['get'],
        permission_classes=[IsAuthenticated, IsEmployer]
    )
    def applicants(self, request, pk=None):
        job = self.get_object()

        # Check ownership - only the job creater(employer) can view applicants
        if job.created_by != request.user:
            return Response(
                {
                    "detail": (
                        "You do not have permission to view",
                        " applicants for this job."
                    )
                },
                status=403
            )

        applications = job.applications.select_related('applicant')
        serializer = ApplicantSerializer(applications, many=True)
        return Response(serializer.data)


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


class MyApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsApplicant]

    def get_queryset(self):
        return Application.objects.filter(
            applicant=self.request.user
        ).select_related('job')
