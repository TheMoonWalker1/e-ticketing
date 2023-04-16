from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    birthday = models.DateField(blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = "User"

    def __str__(self):
        return self.username