from django.db import models

import sheetmusic.models


class Repertoire(models.Model):
    """Model representing a repertoire"""

    title = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return self.title


class RepertoireEntry(models.Model):
    """Model representing a score entry in a repertoire"""

    repertoire = models.ForeignKey(
        Repertoire, on_delete=models.CASCADE, related_name="entries"
    )
    score = models.ForeignKey(
        sheetmusic.models.Score,
        on_delete=models.CASCADE,
        related_name="repertoireEntries",
    )

    def __str__(self):
        return f"{self.repertoire} - {self.score}"
