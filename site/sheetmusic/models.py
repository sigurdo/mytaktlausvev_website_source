""" Models for the sheetmusic-app """

import os, shutil
import django
from django.db import models
from django.contrib.auth.models import User
from upload_validator import FileTypeValidator

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
    file = models.FileField(upload_to='sheetmusic/original_pdfs/', default=None, validators=[FileTypeValidator(
        allowed_types=["application/pdf", "application/x-pdf", "application/x-bzpdf", "application/x-gzpdf"],
        allowed_extensions=[".pdf", ".PDF"])])
    timestamp = models.DateTimeField()

@django.dispatch.receiver(django.db.models.signals.pre_delete, sender=Pdf, dispatch_uid="pdf_delete_images")
def pdf_pre_delete_receiver(sender, instance: Pdf, using, **kwargs):
    # Deleting all images related to that pdf
    if os.path.exists(os.path.join(django.conf.settings.MEDIA_ROOT, 'sheetmusic', 'images', str(instance.pk))):
        shutil.rmtree(os.path.join(django.conf.settings.MEDIA_ROOT, 'sheetmusic', 'images', str(instance.pk)))
    # Deleting actual pdf file
    if os.path.isfile(instance.file.path):
        os.remove(instance.file.path)

class Part(models.Model):
    """ Model representing a part """
    name = models.CharField(max_length=255)
    pdf = models.ForeignKey(Pdf, on_delete=models.CASCADE)
    fromPage = models.IntegerField(default=None)
    toPage = models.IntegerField(default=None)
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
