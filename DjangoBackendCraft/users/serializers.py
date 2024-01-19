from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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
    def validate_email(self, value):
        # Obtén el usuario que se está actualizando
        instance = self.instance

        # Verifica si el nuevo correo electrónico ya está en uso por otro usuario
        if instance and instance.email == value:
            # Si el nuevo correo electrónico es el mismo que el actual, no aplicamos la validación
            return value

        # Validación del correo electrónico solo si está cambiando
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('This email is already registered.')
        return value

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']

    # def validate_email(self, value):
    #     # Add additional email validations if needed
    #     if CustomUser.objects.filter(email__iexact=value).exists():
    #         raise serializers.ValidationError('This email is already registered.')
    #     return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        return token