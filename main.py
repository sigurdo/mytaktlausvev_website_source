import os
from os.path import join, splitext

import PIL.Image
import PIL.ImageDraw
import numpy as np

print("hei buttons")

PAGE_WIDTH_MM = 210
PAGE_HEIGHT_MM = 297
PAGE_DPI = 300
PAGE_MARGIN_TOP_MM = 3
PAGE_MARGIN_RIGHT_MM = 3
PAGE_MARGIN_BOTTOM_MM = 3
PAGE_MARGIN_LEFT_MM = 3
BUTTON_WIDTH_MM = 67
BUTTON_HEIGHT_MM = 67
BUTTON_BORDER_MM = 0.5

def mm_to_px(mm):
	return int(PAGE_DPI * (mm / 25.4))

PAGE_WIDTH_PX = mm_to_px(PAGE_WIDTH_MM)
PAGE_HEIGHT_PX = mm_to_px(PAGE_HEIGHT_MM)
PAGE_MARGIN_TOP_PX = mm_to_px(PAGE_MARGIN_TOP_MM)
PAGE_MARGIN_RIGHT_PX = mm_to_px(PAGE_MARGIN_RIGHT_MM)
PAGE_MARGIN_BOTTOM_PX = mm_to_px(PAGE_MARGIN_BOTTOM_MM)
PAGE_MARGIN_LEFT_PX = mm_to_px(PAGE_MARGIN_LEFT_MM)
BUTTON_WIDTH_PX = mm_to_px(BUTTON_WIDTH_MM)
BUTTON_HEIGHT_PX = mm_to_px(BUTTON_HEIGHT_MM)
BUTTON_BORDER_PX = mm_to_px(BUTTON_BORDER_MM)

NUM_BUTTONS_HORIZONTAL = (PAGE_WIDTH_PX - PAGE_MARGIN_LEFT_PX - PAGE_MARGIN_RIGHT_PX) // BUTTON_WIDTH_PX
NUM_BUTTONS_VERTICAL = (PAGE_HEIGHT_PX - PAGE_MARGIN_TOP_PX - PAGE_MARGIN_BOTTOM_PX) // BUTTON_HEIGHT_PX

ARRAY_LEFT_PX = (PAGE_WIDTH_PX - (NUM_BUTTONS_HORIZONTAL * BUTTON_WIDTH_PX)) // 2
ARRAY_TOP_PX = (PAGE_HEIGHT_PX - (NUM_BUTTONS_VERTICAL * BUTTON_HEIGHT_PX)) // 2

print(f"number of buttons: {NUM_BUTTONS_HORIZONTAL * NUM_BUTTONS_VERTICAL} ({NUM_BUTTONS_HORIZONTAL}x{NUM_BUTTONS_VERTICAL})")


INPUT_PATH = "input_images"
OUTPUT_PATH = "output_pdfs"

for (dirpath, dirnames, filenames) in os.walk(INPUT_PATH):
    for filename in filenames:
        img = PIL.Image.open(join(dirpath, filename), "r")
        img = img.resize((BUTTON_WIDTH_PX, BUTTON_HEIGHT_PX))
        img_width, img_height = img.size
        PIL.ImageDraw.Draw(img).ellipse([(0, 0), (BUTTON_WIDTH_PX, BUTTON_HEIGHT_PX)], width=BUTTON_BORDER_PX, outline=(0, 0, 0, 255))

        mask = PIL.Image.new("RGBA", (BUTTON_WIDTH_PX, BUTTON_HEIGHT_PX), (255, 255, 255, 255))
        PIL.ImageDraw.Draw(mask).ellipse([(0, 0), (BUTTON_WIDTH_PX, BUTTON_HEIGHT_PX)], fill=(0, 0, 0, 0))
        img.paste(mask.copy(), (0, 0), mask=mask.copy())

        background = PIL.Image.new("RGBA", (PAGE_WIDTH_PX, PAGE_HEIGHT_PX), (255, 255, 255, 255))
        for i in range(NUM_BUTTONS_HORIZONTAL):
            for j in range(NUM_BUTTONS_VERTICAL):
                offset_left = ARRAY_LEFT_PX + (i * BUTTON_WIDTH_PX)
                offset_top = ARRAY_TOP_PX + (j * BUTTON_HEIGHT_PX)
                background.paste(img.copy(), (offset_left, offset_top), mask=img.copy())
        output_path = join(OUTPUT_PATH, f"{splitext(filename)[0]}.pdf")
        background.convert("RGB").save(output_path, format="PDF", resolution=PAGE_DPI)
        print("pdf written:", output_path)
