from datetime import datetime

from django.db import models

from config import settings
from core.user.models import User


class WhoCreatedIt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    time_joined = models.TimeField(default=datetime.now)
    class Meta:
        abstract = True

class BaseModel(models.Model):
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_updated',
                                     null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
