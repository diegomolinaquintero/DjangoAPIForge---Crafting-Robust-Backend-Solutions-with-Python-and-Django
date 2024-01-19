from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CreateUserView, UserDetailsView, UserUpdateView, UserDeleteView, ChangePasswordView , CustomTokenObtainPairView,ResetPasswordView,PasswordResetConfirmView

urlpatterns = [
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('details_user/<int:id>/', UserDetailsView.as_view(), name='user_details'),
    path('update_user/<int:id>/', UserUpdateView.as_view(), name='user_update'),
    path('delete_user/<int:id>/', UserDeleteView.as_view(), name='user_delete'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='change_password'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset-password/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]