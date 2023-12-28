from django.db import models

from django.db import models
from users.models import CustomUser

class UserSearchHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    search_query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


