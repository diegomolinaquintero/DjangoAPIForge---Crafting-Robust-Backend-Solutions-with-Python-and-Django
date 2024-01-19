from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, PasswordResetConfirmSerializer
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password,check_password
from .utils import get_tokens_for_user
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode


'''
{
    "email": [
        "Enter a valid email address."
    ],
    "first_name": [
        "First name must have at least 3 characters.",
        "First name must contain only letters.",
        "First name cannot start with a number."
    ],
    "last_name": [
        "Last name must have at least 3 characters.",
        "Last name must contain only letters.",
        "Last name cannot start with a number."
    ],
    "password": [
        "This password is too short. It must contain at least 8 characters.",
        "This password is too common.",
        "This password is entirely numeric."
    ]
}
'''

class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data.get('password'))
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailsView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'id' 

class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'id'
    

class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    lookup_field = 'id'
    def destroy(self, request, *args, **kwargs):
        # instance = self.get_object()
        # self.perform_destroy(instance)  #Forma rapida de borrar todo
        # return Response(status=status.HTTP_204_NO_CONTENT)
        instance = self.get_object()
        confirm_delete = request.query_params.get('confirm_delete', '').lower()
        print("confirm_delete:", confirm_delete)
        print(confirm_delete)
        print(request)
        print(instance)
        if confirm_delete == 'true':
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif confirm_delete == 'false':
            return Response({"detail": "Deletion not confirmed. The user will not be deleted."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Please specify 'confirm_delete=true' or 'confirm_delete=false' to confirm or deny the deletion of the user."}, status=status.HTTP_400_BAD_REQUEST)
        
class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        current_password = request.data.get('current_password')
        print(check_password(current_password, instance.password))
        if not check_password(current_password, instance.password):
            return Response({"detail": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        if new_password != confirm_password:
            return Response({"detail": "New password and confirmation do not match."}, status=status.HTTP_400_BAD_REQUEST)

        instance.password = make_password(new_password)
        instance.save()

        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
    

class ResetPasswordView(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            print(email)# Utiliza CustomUser
        except CustomUser.DoesNotExist:
            return Response({"detail": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        current_site = get_current_site(request)
        domain = current_site.domain

        reset_password_url = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
        reset_password_url = 'http://' + domain + reset_password_url

        email_subject = 'Reset your password'
        email_body = f'Click the following link to reset your password:\n\n{reset_password_url}'

        email = EmailMessage(
            email_subject,
            email_body,
            to=[email],
        )
        email.send()

        return Response({"detail": "Password reset email sent successfully."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(generics.UpdateAPIView):
    serializer_class = PasswordResetConfirmSerializer
    def update(self, request, *args, **kwargs):
        uidb64 = kwargs['uidb64']
        token = kwargs['token']

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)  # Utiliza CustomUser
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')

            if new_password != confirm_password:
                return Response({"detail": "New password and confirmation do not match."}, status=status.HTTP_400_BAD_REQUEST)

            user.password = make_password(new_password)
            user.save()

            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid password reset link."}, status=status.HTTP_400_BAD_REQUEST)
    
class CustomTokenObtainPairView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        if email:
            CustomUser = get_user_model()

            try:
                user = CustomUser.objects.get(email=email)
                if not user.is_active:
                    return Response({'error': 'Usuario inactivo.'}, status=400)
                
                tokens = get_tokens_for_user(user)

                return Response(tokens)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Usuario no encontrado.'}, status=404)

        return Response({'error': 'Se requiere el campo "email" en la solicitud.'}, status=400)
