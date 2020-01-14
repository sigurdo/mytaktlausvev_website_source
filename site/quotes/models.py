from django.db import models

# Create your models here.

class Quote(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=2000)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.text