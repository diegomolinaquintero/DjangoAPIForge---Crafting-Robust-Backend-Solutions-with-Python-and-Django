from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

