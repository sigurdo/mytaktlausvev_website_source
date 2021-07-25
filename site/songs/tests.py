from django.test import TestCase
from .models import Song


class SongTestCase(TestCase):
    def setUp(self):
        self.song = Song.objects.create(
            title="Song of Tests", lyrics="Test, test, test"
        )

    def test_song_to_string_equals_title(self):
        """Song's to string method should return the song's title."""
        self.assertEqual(str(self.song), self.song.title)
