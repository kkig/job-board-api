from rest_framework import serializers
from .models import Application


# Convert model to JSON format
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'job', 'cover_letter', 'applied_at']
        read_only_fields = ['id', 'applied_at', 'job']
