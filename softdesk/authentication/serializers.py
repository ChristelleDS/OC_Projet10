from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer, ValidationError
from .models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'password', 'email', 'first_name', 'last_name']

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value).exists():
            raise ValidationError("User already exists")
        return value

    def validate_password(self, value: str) -> str:
        if value is not None:
            return make_password(value)
        raise ValidationError("Password is empty")
