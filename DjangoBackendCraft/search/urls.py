from django.urls import path

from .views import UserListView, UserSearchView


urlpatterns = [
    path('list_users/', UserListView.as_view(), name='list_user'),
    path('search_user/', UserSearchView.as_view(), name='user-search'),
]
