from django.db import models
from django.conf import settings

# Create your models here.
class Link(models.Model):
    url = models.URLField()
    # blank=True allows the field to be blank, default is set to False
    description = models.TextField(blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
