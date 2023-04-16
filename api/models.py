from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=12, blank=False, null=False, unique=True, primary_key=True)
    sex = models.CharField(max_length=50, null=True)
    birthday = models.DateField(blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    password = None
    # picture = models.

    class Meta:
        verbose_name_plural = "User"

    def __str__(self):
        return self.username