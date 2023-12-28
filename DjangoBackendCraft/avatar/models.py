from django.db import models

from django.db import models
from users.models import CustomUser

class UserAvatar(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
