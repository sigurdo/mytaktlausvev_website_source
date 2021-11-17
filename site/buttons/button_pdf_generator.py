from math import ceil
import io

import PIL.Image
import PIL.ImageDraw


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
    button_width_mm=67,
    button_height_mm=67,
    button_border_mm=0.5,
):
    def mm_to_px(mm):
        return int(page_dpi * (mm / 25.4))

    page_width_px = mm_to_px(page_width_mm)
    page_height_px = mm_to_px(page_height_mm)
    page_margin_top_px = mm_to_px(page_margin_top_mm)
    page_margin_right_px = mm_to_px(page_margin_right_mm)
    page_margin_bottom_px = mm_to_px(page_margin_bottom_mm)
    page_margin_left_px = mm_to_px(page_margin_left_mm)
    button_width_px = mm_to_px(button_width_mm)
    button_height_px = mm_to_px(button_height_mm)
    button_border_px = mm_to_px(button_border_mm)

    num_buttons_horizontal = (
        page_width_px - page_margin_left_px - page_margin_right_px
    ) // button_width_px
    num_buttons_vertical = (
        page_height_px - page_margin_top_px - page_margin_bottom_px
    ) // button_height_px
    num_buttons_per_page = num_buttons_horizontal * num_buttons_vertical
    num_pages = ceil(len(images) * num_of_each / num_buttons_per_page)

    array_left_px = (page_width_px - (num_buttons_horizontal * button_width_px)) // 2
    array_top_px = (page_height_px - (num_buttons_vertical * button_height_px)) // 2

    pages = []

    for p in range(num_pages):
        background = PIL.Image.new(
            "RGBA", (page_width_px, page_height_px), (255, 255, 255, 255)
        )
        mask = PIL.Image.new(
            "RGBA", (button_width_px, button_height_px), (255, 255, 255, 255)
        )
        PIL.ImageDraw.Draw(mask).ellipse(
            [(0, 0), (button_width_px, button_height_px)], fill=(0, 0, 0, 0)
        )
        for r in range(num_buttons_vertical):
            break_nested_for_loop = False
            for c in range(num_buttons_horizontal):
                images_index = (
                    num_buttons_per_page * p + num_buttons_horizontal * r + c
                ) // num_of_each
                if images_index >= len(images):
                    break_nested_for_loop = True
                    break
                img = images[images_index].convert("RGBA")
                img = img.resize((button_width_px, button_height_px))
                img_width, img_height = img.size
                PIL.ImageDraw.Draw(img).ellipse(
                    [(0, 0), (button_width_px, button_height_px)],
                    width=button_border_px,
                    outline=(0, 0, 0, 255),
                )
                img.paste(mask.copy(), (0, 0), mask=mask.copy())

                offset_left = array_left_px + (c * button_width_px)
                offset_top = array_top_px + (r * button_height_px)
                background.paste(img.copy(), (offset_left, offset_top), mask=img.copy())
            if break_nested_for_loop:
                break
        pages.append(background)

    output_bytes = io.BytesIO()
    if len(pages) > 1:
        pages[0].convert("RGB").save(
            output_bytes,
            format="PDF",
            resolution=page_dpi,
            save_all=True,
            append_images=[page.convert("RGB") for page in pages[1:]],
        )
    else:
        pages[0].convert("RGB").save(output_bytes, format="PDF", resolution=page_dpi)
    return output_bytes
