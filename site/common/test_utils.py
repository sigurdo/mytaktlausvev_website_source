from django.core.files.uploadedfile import SimpleUploadedFile


def test_image_gif_2x2():
    """Returns a temporary image file (2x2 black pixels) that can be used in tests."""
    gif = b"GIF89a\x02\x00\x02\x00p\x00\x00,\x00\x00\x00\x00\x02\x00\x02\x00\x81\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x02\x84Q\x00;"
    return SimpleUploadedFile(
        name="test_image.gif",
        content=gif,
        content_type="image/gif",
    )


def create_formset_post_data(
    total_forms=2,
    initial_forms=1,
    min_num_forms=0,
    max_num_forms=1000,
    formset_class=None,
    defaults=None,
    forms=None,
):
    """
    Inputs:
    - total_forms
    - initial_forms
    - min_num_forms
    - max_num_forms
    - defaults - a dictionary on the format {"field": "default"} of default values for the fields
    - forms - a list of dictionaries on the format {"field": "value"} that provide the actual values to use for the fields in each subform

    Returns a dictonary which is the post data for the formset

    How it works:

    It is always total_forms that tell how many forms the post data will be generated for

    All forms will have the same fields. These fields are selected from the input in the following priority:
    1. The fields in the form of the formset_class
    2. The keys in the defaults dict
    3. The keys in the 0th element of the forms list
    4. If none of the above were found, it raises and exception

    Then it fills out values for initial_forms number of forms with the following priority:
    1. The value from the corresponding index and field in the forms list
    2. The value from the corresponding field in the defaults dict
    3. The value ""

    And finally fils out values up to total_forms number of forms with the following priority:
    1. The value from the corresponding index and field in the forms list
    2. The value ""

    For details on how fields are named, it is recommended to inspect the post request in developer tools in your browser
    """
    if formset_class is not None:
        fields = list(formset_class.form.base_fields.keys())
    elif defaults is not None:
        fields = list(defaults.keys())
    elif forms is not None and len(forms) > 0:
        fields = list(forms[0].keys())
    else:
        raise Exception("Must configure either formset_class, defaults or forms")
    if "id" not in fields:
        fields.append("id")
    if "DELETE" not in fields:
        fields.append("DELETE")
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
            elif field in defaults:
                # Use default value if no provided form field and it is not and extra form
                value = defaults[field]
            else:
                # Use nothing if not even a default value is provided
                value = ""
            result[f"form-{i}-{field}"] = value
    return result
