from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    JobViewSet,
    SignupView,
    MyApplicationsView,
    MyJobsView,
    my_profile,
)

router = DefaultRouter()    # Generates RESTful URLs automatically
router.register(r'jobs', JobViewSet, basename='job')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', SignupView.as_view(), name='user-register'),
    path(
        'my-applications/',
        MyApplicationsView.as_view(),
        name='my-applications'
    ),
    path('my-jobs/', MyJobsView.as_view(), name='my-jobs'),
    path('profile/', my_profile, name='my-profile'),
]
