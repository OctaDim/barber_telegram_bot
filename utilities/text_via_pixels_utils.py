from PIL import Image, ImageDraw, ImageFont
import os


def get_text_pixel_width_else_len(text_string: str) -> int:
    # Trying to load system default font
    try:
        font = ImageFont.load_default()
    except IOError as error:
        print(f"\tTEST INFO: Loading default system font failed: {error}")
        return len(text_string)

    # Creating temporary image canvas 1х1 pixels
    image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)

    # Getting text width in pixels via img canvas (for system default font)
    text_pixels_width = draw.textlength(text_string, font=font)
    text_pixels_width = int(text_pixels_width)
    return text_pixels_width


def get_fill_symbols_number_via_pixels(text_long: str = "",
                                       text_short: str = "",
                                       fill_symbol: str = "") -> int:
    if not fill_symbol or len(text_long) <= len(text_short):
        return 0

    text_long_pxl_width = get_text_pixel_width_else_len(
        text_string=text_long)

    text_short_pxl_width = get_text_pixel_width_else_len(
        text_string=text_short)

    fill_symbol_pxl_width = get_text_pixel_width_else_len(
        text_string=fill_symbol)

    texts_pxl_width_delta = text_long_pxl_width - text_short_pxl_width

    fill_symbols_number = texts_pxl_width_delta / fill_symbol_pxl_width
    fill_symbols_number = int(round(fill_symbols_number, 0))
    return fill_symbols_number
