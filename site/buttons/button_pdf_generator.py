import io
from math import ceil

import PIL.Image
import PIL.ImageDraw


def pages_to_pdf(pages: list, page_dpi=300) -> io.BytesIO:
    """
    Input:
    - pages: a list of PIL.Image objects, one for each page in the PDF

    Returns:
    - An io.BytesIO object containing the pdf file
    """
    pages = [page.convert("RGB") for page in pages]
    output_bytes = io.BytesIO()
    if len(pages) > 1:
        pages[0].save(
            output_bytes,
            format="PDF",
            resolution=page_dpi,
            save_all=True,
            append_images=pages[1:],
        )
    else:
        pages[0].save(output_bytes, format="PDF", resolution=page_dpi)
    output_bytes.seek(0)
    return output_bytes


def button_pdf_generator(
    images,
    num_of_each=1,
    page_width_mm=210,
    page_height_mm=297,
    page_dpi=300,
    page_margin_top_mm=3,
    page_margin_right_mm=3,
    page_margin_bottom_mm=3,
    page_margin_left_mm=3,
    button_visible_width_mm=57,
    button_visible_height_mm=57,
    button_backside_padding_mm=5,
    button_minimum_distance_mm=0,
    button_outline_mm=0.5,
):
    """
    Input:
    - images: a list of PIL image objects
    - kwargs: layout parameters

    Returns:
    - An io.BytesIO object containing the output pdf file
    """

    def mm_to_px(mm):
        """
        Converts a number of mm to a number of pixels based on page_dpi
        """
        return int(page_dpi * (mm / 25.4))

    # Calculate input parameters in pixels
    page_width_px = mm_to_px(page_width_mm)
    page_height_px = mm_to_px(page_height_mm)
    page_margin_top_px = mm_to_px(page_margin_top_mm)
    page_margin_right_px = mm_to_px(page_margin_right_mm)
    page_margin_bottom_px = mm_to_px(page_margin_bottom_mm)
    page_margin_left_px = mm_to_px(page_margin_left_mm)
    button_full_width_px = mm_to_px(
        button_visible_width_mm + 2 * button_backside_padding_mm
    )
    button_full_height_px = mm_to_px(
        button_visible_height_mm + 2 * button_backside_padding_mm
    )
    button_minimum_distance_px = mm_to_px(button_minimum_distance_mm)
    button_outline_px = mm_to_px(button_outline_mm)

    # Calculate dependent parameter based on input parameters

    num_buttons_horizontal = (
        page_width_px
        - page_margin_left_px
        - page_margin_right_px
        - button_minimum_distance_px
    ) // (button_full_width_px + button_minimum_distance_px)
    num_buttons_vertical = (
        page_height_px
        - page_margin_top_px
        - page_margin_bottom_px
        - button_minimum_distance_px
    ) // (button_full_height_px + button_minimum_distance_px)
    num_buttons_per_page = num_buttons_horizontal * num_buttons_vertical
    num_pages = ceil(len(images) * num_of_each / num_buttons_per_page)
    array_left_px = (
        page_width_px
        - (num_buttons_horizontal * button_full_width_px)
        - ((num_buttons_horizontal - 1) * button_minimum_distance_px)
    ) // 2
    array_top_px = (
        page_height_px
        - (num_buttons_vertical * button_full_height_px)
        - ((num_buttons_vertical - 1) * button_minimum_distance_px)
    ) // 2

    # List of pages to append to in for loop
    pages = []

    for p in range(num_pages):
        # Make a white background
        background = PIL.Image.new(
            "RGBA", (page_width_px, page_height_px), (255, 255, 255, 255)
        )

        # Make white peripheral
        white_peripheral = PIL.Image.new(
            "RGBA", (button_full_width_px, button_full_height_px), (255, 255, 255, 255)
        )
        PIL.ImageDraw.Draw(white_peripheral).ellipse(
            [(0, 0), (button_full_width_px, button_full_height_px)], fill=(0, 0, 0, 0)
        )

        def paint_page():
            for r in range(num_buttons_vertical):
                for c in range(num_buttons_horizontal):
                    # Calculate index to get from the images list
                    images_index = (
                        num_buttons_per_page * p + num_buttons_horizontal * r + c
                    ) // num_of_each
                    if images_index >= len(images):
                        return

                    # Get image from list, convert and scale
                    img = images[images_index]
                    img = img.convert("RGBA")
                    img = img.resize((button_full_width_px, button_full_height_px))

                    # Draw outline
                    PIL.ImageDraw.Draw(img).ellipse(
                        [(0, 0), (button_full_width_px, button_full_height_px)],
                        width=button_outline_px,
                        outline=(0, 0, 0, 255),
                    )

                    # Make image white outside outline
                    img.paste(
                        white_peripheral.copy(), (0, 0), mask=white_peripheral.copy()
                    )

                    # Calculate position on page
                    offset_left = array_left_px + (
                        c * (button_full_width_px + button_minimum_distance_px)
                    )
                    offset_top = array_top_px + (
                        r * (button_full_height_px + button_minimum_distance_px)
                    )

                    background.paste(
                        img.copy(), (offset_left, offset_top), mask=img.copy()
                    )

        paint_page()
        pages.append(background)

    return pages_to_pdf(pages, page_dpi=page_dpi)
