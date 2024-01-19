from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user_id': user.id,
        'user_email': user.email,
        'user_first_name': user.first_name,
        'user_last_name': user.last_name,
    }
