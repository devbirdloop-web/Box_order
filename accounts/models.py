from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    full_name = models.CharField(max_length=200, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def is_admin(self):
        return self.role == 'admin'