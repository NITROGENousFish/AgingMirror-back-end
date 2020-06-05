from django.db import models
from django.utils import timezone


class User(models.Model):
    openid = models.CharField(max_length=50, unique=True,primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)

class Album(models.Model):
    nickname = models.BinaryField(max_length=300)
    albumname = models.CharField(max_length=50)
    visibility =models.BooleanField()
    createtime = models.DateTimeField()
    totalsum = models.IntegerField()