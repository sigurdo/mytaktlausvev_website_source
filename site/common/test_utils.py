from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image, ImageDraw


def test_txt_file(name="test.txt", content="test", content_type="text/plain"):
    return SimpleUploadedFile(
        name=name,
        content=bytes(content, "utf-8"),
        content_type=content_type,
    )


def test_image(name="test_image.gif", content_type="image/gif"):
    """Returns a temporary image file that can be used in tests."""
    gif = b"GIF89a\x02\x00\x02\x00p\x00\x00,\x00\x00\x00\x00\x02\x00\x02\x00\x81\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x02\x84Q\x00;"
    return SimpleUploadedFile(
        name=name,
        content=gif,
        content_type=content_type,
    )


def test_pdf(name="test.pdf", content_type="application/pdf"):
    """Returns a temporary pdf file with 1 page and the text Tuba written to the top left that can be used in tests."""
    return test_pdf_multipage(["Tuba"], name=name, content_type=content_type)


def test_pdf_multipage(
    page_titles, name="multipage.pdf", content_type="application/pdf"
):
    """
    Returns a temporary pdf file with one page per element in page_titles, with titles written
    to the top left on each page.
    """
    imgs = []
    for page_title in page_titles:
        img = Image.new("L", (500, 707), 255)
        ImageDraw.Draw(img).text((50, 50), page_title, fill=0)
        imgs.append(img)
    pdf = BytesIO()
    imgs[0].save(
        pdf, resolution=67, format="PDF", save_all=True, append_images=imgs[1:]
    )
    return SimpleUploadedFile(
        name=name,
        content=pdf.getvalue(),
        content_type=content_type,
    )


def create_formset_post_data(
    formset_class,
    defaults={},
    data=[],
    total_forms=2,
    initial_forms=1,
    min_num_forms=0,
    max_num_forms=1000,
):
    """
    Inputs:
    - `formset_class`
    - `defaults`
        - a dictionary with the format {"field": "default"} of default values for the fields
    - `data`
        - a list of dictionaries with the format {"field": "value"} that provides the actual values to use for the fields in each form
    - `total_forms`
    - `initial_forms`
    - `min_num_forms`
    - `max_num_forms`

    Returns a dictonary which is the post data for the formset.

    How it works:

    `total_forms` decides how many forms data will be generated for.

    Values for `initial_forms` number of forms are filled with the following priority:
    1. The value from the corresponding index and field in `data`
    2. The value from the corresponding field in `defaults`
    3. The value ""

    Values up to `total_forms` number of forms are filled with the following priority:
    1. The value from the corresponding index and field in `data`
    2. The value ""

    For details on how fields are named, it is recommended to inspect that particular post request in developer tools in your browser.
    """
    fields = list(formset_class.form.base_fields.keys())
    if "id" not in fields:
        fields.append("id")
    if "DELETE" not in fields:
        fields.append("DELETE")

    form_prefix = formset_class().prefix
    result = {
        f"{form_prefix}-TOTAL_FORMS": total_forms,
        f"{form_prefix}-INITIAL_FORMS": initial_forms,
        f"{form_prefix}-MIN_NUM_FORMS": min_num_forms,
        f"{form_prefix}-MAX_NUM_FORMS": max_num_forms,
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

            result[f"{form_prefix}-{i}-{field}"] = value
    return result
