from django.urls import path

from .views import BlockUserView, UnblockUserView


urlpatterns = [
    path('block_user/<int:user_id>/', BlockUserView.as_view(), name='block_user'),
    path('unblock_user/<int:user_id>/', UnblockUserView.as_view(), name='Unblock_user'),
]
