from django.urls import path
from .views import UserStatsView

urlpatterns = [
    path('stats/', UserStatsView.as_view(), name='user_stats'),
]