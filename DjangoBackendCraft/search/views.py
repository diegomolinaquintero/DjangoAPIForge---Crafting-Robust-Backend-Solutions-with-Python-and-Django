from django.shortcuts import render

from rest_framework import generics
from .models import CustomUser
from users.serializers import CustomUserSerializer

from django.db.models import Q
from users.models import CustomUser

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
class UserSearchView(generics.ListAPIView):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        search_term = self.request.query_params.get('search', '')
        return CustomUser.objects.filter(
            Q(email__icontains=search_term) |
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term)
        )