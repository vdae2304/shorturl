from django.db import models

# Create your models here.
class ShortURLs(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=255)
    shorturl = models.CharField(max_length=10, unique=True)
    creator = models.IntegerField(default=None)
    token = models.CharField(max_length=20, default=None)