from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.ImageField(upload_to='accounts/%Y/%m/%d', blank=True, null=True, verbose_name='Фото')
    bio = models.CharField(blank=True, null=True, verbose_name='Описание')

