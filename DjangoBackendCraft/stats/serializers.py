from rest_framework import serializers
from users.models import CustomUser

class UserStatsSerializer(serializers.Serializer):
    total_users = serializers.SerializerMethodField()
    active_users = serializers.SerializerMethodField()
    blocked_users = serializers.SerializerMethodField()

    def get_total_users(self, obj):
        return CustomUser.objects.count()

    def get_active_users(self, obj):
        return CustomUser.objects.filter(is_active=True).count()

    def get_blocked_users(self, obj):
        return CustomUser.objects.filter(is_active=False).count()