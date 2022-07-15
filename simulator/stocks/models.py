from django.db import models
from core import settings

class StockDetail(models.Model):
    stock = models.CharField(max_length=255, unique=True)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)
