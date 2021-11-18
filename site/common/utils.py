from django.core.files.uploadedfile import SimpleUploadedFile


def test_image():
    """Returns a temporary image file that can be used in tests."""
    gif = b"GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x00;"
    return SimpleUploadedFile(
        name="test_image.gif",
        content=gif,
        content_type="image/gif",
    )
