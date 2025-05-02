from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import JobViewSet, SignupView

router = DefaultRouter()    # Generates RESTful URLs automatically
router.register(r'jobs', JobViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', SignupView.as_view(), name='user-register'),
]
