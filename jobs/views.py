from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import AllowAny

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
