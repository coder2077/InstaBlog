from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
	bio = models.CharField(max_length=150)
	profile_pic = models.ImageField(upload_to='images/', null=True, blank=True)

