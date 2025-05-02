from rest_framework import serializers
from .models import Job


# Convert model instances to JSON format
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job     # Includes all fields from Job model
        fields = '__all__'
