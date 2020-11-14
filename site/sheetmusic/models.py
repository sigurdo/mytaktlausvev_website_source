""" Models for the sheetmusic-app """

from django.db import models
from django.contrib.auth.models import User

class Score(models.Model):
    """ Model representing a score """
    title = models.CharField(max_length=255)
    # description = models.CharField(max_length=2000)
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return self.title

class Pdf(models.Model):
    """ Model representing an uploaded pdf """
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

class Part(models.Model):
    """ Model representing a part """
    pdf = models.ForeignKey(Pdf, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

class Instrument(models.Model):
    """ Model representing an instrument """
    name = models.CharField(max_length=255)

class InstrumentsPreferredPart(models.Model):
    """ Model representing the preferred part of an instrument """
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)

class UsersPreferredPart(models.Model):
    """ Model representing the preferred part of a user """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
