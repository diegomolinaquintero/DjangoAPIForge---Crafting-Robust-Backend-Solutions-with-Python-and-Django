from rest_framework import generics
from .serializers import UserStatsSerializer
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated

class UserStatsView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserStatsSerializer
    def get_object(self):
        return CustomUser.objects.first()  # You can use any user object since the statistics are not specific to a user
