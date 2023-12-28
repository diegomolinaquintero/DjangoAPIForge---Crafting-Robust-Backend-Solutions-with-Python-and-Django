from django.db import models

from django.db import models
from users.models import CustomUser

class BlockedUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_blocked = models.BooleanField(default=False)


