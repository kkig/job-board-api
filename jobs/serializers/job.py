from rest_framework import serializers
from jobs.models import Job


# Convert model instances to JSON format
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job     # Includes all fields from Job model
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'posted_at']
