from rest_framework import (
    viewsets,
    permissions,
    generics,
    status,
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes

from rest_framework_simplejwt.tokens import RefreshToken

from django.shortcuts import get_object_or_404

from .models import Job, Application

from .serializers import JobSerializer
from .serializers import UserSignupSerializer
from .serializers import ApplicationSerializer
from .serializers import ProfileSerializer

from .permissions import IsEmployer, IsApplicant

from .tasks import send_application_notification


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
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['patch'],
        permission_classes=[IsAuthenticated, IsEmployer]
    )
    def update_status(self, request, pk=None):
        job = self.get_object()
        if job.created_by != request.user:
            return Response({"detail": "Not allowed"}, status=403)

        app_id = request.data.get('application_id')
        new_status = request.data.get('status')

        if new_status not in ['pending', 'accepted', 'rejected']:
            return Response({"detail": "Invalid status"}, status=400)

        try:
            application = job.applications.get(id=app_id)
        except Application.DoesNotExist:
            return Response({"detail": "Application not found"}, status=404)

        application.status = new_status
        application.save()

        return Response(
            {"detail": "Status updated"},
            status=status.HTTP_200_OK
        )


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


class MyJobsView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        return Job.objects.filter(
                created_by=self.request.user
            ).order_by('-posted_at')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    """
    View current user's profile
    """
    profile = request.user.profile
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes
def apply_to_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Check if the user has already applied
    if Application.objects.filter(user=request.user, job=job).exists():
        return Response(
            {"detail": "You have already applied to this job."},
            status=400
            )

    # Create the application
    application = Application.objects.create(
        user=request.user,
        job=job,
        status='Applied'
    )

    print("Triggering application notification")
    
    # Trigger the email notification asynchronously via Celery
    send_application_notification.delay(
        to_email=job.created_by.email,
        job_title=job.title,
        applicant_name=request.user.username
    )

    serializer = ApplicationSerializer(application)

    return Response(
        serializer.data,
        status=201,
        )
