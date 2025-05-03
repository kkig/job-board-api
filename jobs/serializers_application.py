from rest_framework import serializers
from .models import Application


# Convert model to JSON format
class ApplicationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='applicant.username')
    email = serializers.EmailField(source='applicant.email')    # Optional
    cover_letter = serializers.CharField()
    applied_at = serializers.DateTimeField()
    job_title = serializers.CharField(source='job.title', read_only=True)
    job_company = serializers.CharField(source='job.company', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'username',
            'email',
            'job',
            'job_title',
            'job_company',
            'cover_letter',
            'applied_at',
            'status'
        ]
        read_only_fields = [
            'id',
            'username',
            'email',
            'applied_at',
            'job',
            'status'
        ]
