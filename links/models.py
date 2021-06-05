from django.db import models

# Create your models here.
class Link(models.Model):
    url = models.URLField()
    # blank=True allows the field to be blank, default is set to False
    description = models.TextField(blank=True)

    def __str__(self):
        return self.description
