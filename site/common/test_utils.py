from django.core.files.uploadedfile import SimpleUploadedFile


def test_image_gif_2x2():
    """Returns a temporary image file (2x2 black pixels) that can be used in tests."""
    gif = b"GIF89a\x02\x00\x02\x00p\x00\x00,\x00\x00\x00\x00\x02\x00\x02\x00\x81\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x02\x84Q\x00;"
    return SimpleUploadedFile(
        name="test_image.gif",
        content=gif,
        content_type="image/gif",
    )
