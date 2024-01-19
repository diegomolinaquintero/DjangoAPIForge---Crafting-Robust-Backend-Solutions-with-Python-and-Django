# users/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from users.models import CustomUser
from .serializers import BlockUserSerializer, UnblockUserSerializer

class BlockUserView(generics.UpdateAPIView):
    serializer_class = BlockUserSerializer

    def update(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        user = CustomUser.objects.get(id=user_id)
        user.is_active = False
        user.save()
        return Response({"detail": "User blocked successfully."}, status=status.HTTP_200_OK)

class UnblockUserView(generics.UpdateAPIView):
    serializer_class = UnblockUserSerializer

    def update(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        user = CustomUser.objects.get(id=user_id)
        # Add logic for unblocking the user
        user.is_active = True
        user.save()
        return Response({"detail": "User unblocked successfully."}, status=status.HTTP_200_OK)

