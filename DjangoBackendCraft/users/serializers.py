from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        max_length=30,
        validators=[
            MinLengthValidator(3, 'First name must have at least 3 characters.'),
            MaxLengthValidator(30, 'First name cannot have more than 30 characters.'),
            RegexValidator(
                regex=r'^[a-zA-Z]+$',
                message='First name must contain only letters.',
                code='invalid_first_name'
            ),
            RegexValidator(
                regex=r'^[^0-9]',
                message='First name cannot start with a number.',
                code='invalid_first_name_start'
            ),
        ]
    )
    last_name = serializers.CharField(
        max_length=30,
        validators=[
            MinLengthValidator(3, 'Last name must have at least 3 characters.'),
            MaxLengthValidator(30, 'Last name cannot have more than 30 characters.'),
            RegexValidator(
                regex=r'^[a-zA-Z]+$',
                message='Last name must contain only letters.',
                code='invalid_last_name'
            ),
            RegexValidator(
                regex=r'^[^0-9]',
                message='Last name cannot start with a number.',
                code='invalid_last_name_start'
            ),
        ]
    )
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']

    def validate_email(self, value):
        # Add additional email validations if needed
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('This email is already registered.')
        return value
