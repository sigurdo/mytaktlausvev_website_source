import os

from django.core.files.uploadedfile import SimpleUploadedFile

from web.settings import BASE_DIR


def test_image_gif_2x2():
    """Returns a temporary image file (2x2 black pixels) that can be used in tests."""
    gif = b"GIF89a\x02\x00\x02\x00p\x00\x00,\x00\x00\x00\x00\x02\x00\x02\x00\x81\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x02\x84Q\x00;"
    return SimpleUploadedFile(
        name="test_image.gif",
        content=gif,
        content_type="image/gif",
    )


def test_pdf():
    """Returns a temporary pdf file with 1 page and the text Tuba written on it that can be used in tests."""
    pdf = open(os.path.join(BASE_DIR, "common", "test_data", "test.pdf"), "rb").read()
    return SimpleUploadedFile(
        name="test.pdf",
        content=pdf,
        content_type="application/pdf",
    )


def create_formset_post_data(
    total_forms=2,
    initial_forms=1,
    min_num_forms=0,
    max_num_forms=1000,
    fields={"field": "default"},
    forms=[],
):
    """
    Inputs:
    fields - a dictionary that declares the fields of each subform as keys and their default values as values
    forms - a list of dictionaries that provide the actual values to use for the fields in each subform

    Returns a dictonary which is the post data for the formset

    If a field is skipped in a form or even the entire form is skipped, the default values from the fields input will be used
    If a form is skipped and the form number is >= initial_forms, blank values will be used instead of the defaults
    """
    result = {
        "form-TOTAL_FORMS": str(total_forms),
        "form-INITIAL_FORMS": str(initial_forms),
        "form-MIN_NUM_FORMS": str(min_num_forms),
        "form-MAX_NUM_FORMS": str(max_num_forms),
    }
    for field in fields:
        result[f"form-__prefix__-{field}"] = ""
    for i in range(total_forms):
        for field in fields:
            if i < len(forms) and field in forms[i]:
                # Use provided form field if it exists
                value = forms[i][field]
            elif i >= initial_forms:
                # Use nothing if no provided form field and it is an extra form
                value = ""
            else:
                # Use default value if no provided form field and it is not and extra form
                value = fields[field]
            result[f"form-{i}-{field}"] = value
    return result
