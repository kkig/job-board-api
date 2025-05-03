from rest_framework import serializers
from .models import Application


class ApplicantSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='applicant.username')
    email = serializers.EmailField(source='applicant.email')    # Optional
    cover_letter = serializers.CharField()
    applied_at = serializers.DateTimeField()

    class Meta:
        model = Application
        fields = ['username', 'email', 'cover_letter', 'applied_at']
