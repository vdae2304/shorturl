from django.db import models
from django.contrib.auth.models import User
import uuid


"""
Token único de usuario para acceder a la REST-API.
"""
class UserTokens(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4)


"""
Lista de URLs acortadas.
"""
class URLs(models.Model):
    id = models.AutoField(primary_key=True)
    long_url = models.CharField(max_length=255)
    short_url = models.CharField(max_length=8, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_private = models.BooleanField(default=False)


"""
Lista de usuarios que tienen permitido acceder a una URL privada.
"""
class URLAllowList(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.ForeignKey(URLs, on_delete=models.CASCADE)


"""
Lista de usuarios que accedieron a una URL.
"""
class URLVisualizations(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    url = models.ForeignKey(URLs, on_delete=models.CASCADE)
