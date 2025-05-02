from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet

router = DefaultRouter()    # Generates RESTful URLs automatically
router.register(r'jobs', JobViewSet)

urlpatterns = [
    path('', include(router.urls))
]
