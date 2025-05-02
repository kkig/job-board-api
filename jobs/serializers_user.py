from django.contrib.auth.models import User
from rest_framework import serializers
from jobs.models import Profile


# Convert model to JSON format
class UserSignupSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        write_only=True
    )
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'password', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # Ensure profile is created and role is assigned
        Profile.objects.filter(user=user).update(role=role)
        return user
