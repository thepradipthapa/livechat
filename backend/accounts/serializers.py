from accounts.models import User
from rest_framework import serializers

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

class UserVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "created_at"]