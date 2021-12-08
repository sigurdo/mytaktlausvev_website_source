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
    formset_class=None,
    defaults=None,
    data=None,
    total_forms=2,
    initial_forms=1,
    min_num_forms=0,
    max_num_forms=1000,
    subform_prefix="form",
):
    """
    Inputs:
    - `formset_class`
    - `defaults` - a dictionary on the format {"field": "default"} of default values for the fields
    - `data` - a list of dictionaries on the format {"field": "value"} that provide the actual values to use for the fields in each subform
    - `total_forms`
    - `initial_forms`
    - `min_num_forms`
    - `max_num_forms`

    Returns a dictonary which is the post data for the formset

    How it works:

    It is always `total_forms` that tell how many forms the post data will be generated for

    All forms will have the same fields. These fields are selected from the input in the following priority:
    1. The fields in the form of the `formset_class`
    2. The keys in `defaults`
    3. The keys in the 0th element of `data`
    4. If none of the above were found, it raises and exception

    Then it fills out values for `initial_forms` number of forms with the following priority:
    1. The value from the corresponding index and field in `data`
    2. The value from the corresponding field in `defaults`
    3. The value ""

    And finally fils out values up to `total_forms` number of forms with the following priority:
    1. The value from the corresponding index and field in `data`
    2. The value ""

    For details on how fields are named, it is recommended to inspect that particular post request in developer tools in your browser
    """
    if formset_class is not None:
        fields = list(formset_class.form.base_fields.keys())
    elif defaults is not None:
        fields = list(defaults.keys())
    elif data is not None and len(data) > 0:
        fields = list(data[0].keys())
    else:
        raise Exception("Must configure either formset_class, defaults or forms")
    if "id" not in fields:
        fields.append("id")
    if "DELETE" not in fields:
        fields.append("DELETE")
    result = {
        f"{subform_prefix}-TOTAL_FORMS": str(total_forms),
        f"{subform_prefix}-INITIAL_FORMS": str(initial_forms),
        f"{subform_prefix}-MIN_NUM_FORMS": str(min_num_forms),
        f"{subform_prefix}-MAX_NUM_FORMS": str(max_num_forms),
    }
    for i in range(total_forms):
        for field in fields:
            if i < len(data) and field in data[i]:
                # Use value from data if it exists
                value = data[i][field]
            elif i < initial_forms and defaults is not None and field in defaults:
                # Use default value if it does not exist in data and it is an initial form
                value = defaults[field]
            else:
                # Use nothing if not even a default value exists
                value = ""

            result[f"{subform_prefix}-{i}-{field}"] = value
    return result
