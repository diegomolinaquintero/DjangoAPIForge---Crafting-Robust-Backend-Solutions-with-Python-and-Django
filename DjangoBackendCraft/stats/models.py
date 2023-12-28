from django.db import models

from django.db import models
from users.models import CustomUser

class UserStatistics(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    total_logins = models.IntegerField(default=0)


