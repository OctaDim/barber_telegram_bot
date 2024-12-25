from dataclasses import dataclass


@dataclass
class IMAGES_LINKS:
    # NOTE: PATHS MUST BE DEFINED FROM CONTENT (PROJECT) ROOT (EXCEPT PROJECT DIRECTORY)
    MAIN_GREETING_IMG: str = r"telegram/images/barber_bot_main_greeting_img_2.jpg"
    MAIN_MENU_IMG: str = r"telegram/images/barber_bot_main_greeting_img_2.jpg"
    # MAIN_GREETING_IMG: str = r"telegram/images/barber_bot_main_greeting_img_1.jpg"
    # MAIN_MENU_IMG: str = r"telegram/images/barber_bot_main_greeting_img_1.jpg"
