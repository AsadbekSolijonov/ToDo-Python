import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from core import settings


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    phone_number = models.CharField(max_length=9, unique=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username}"


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=150, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return f"{self.name}"


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="tasks")
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"
