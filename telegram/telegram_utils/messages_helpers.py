from datetime import timedelta

from database.db_models.service_model import Service
from telegram.config.configs import SLOTS_CONFIGS
from telegram.params.buttons_common import SPECIAL_CHARACTERS
from telegram.params.calendar_icons import CALENDAR_ICONS
from telegram.params.intervals_slots_icons import SLOT_ICONS
from telegram.params.messages import BETTER_SLOTS_TO_CHOOSE, CHOOSE_OTHER_SLOTS, SLOTS_RECOMMENDATIONS
from telegram.params.messages_inserts import MSG
from telegram.params.messages_multiline import SELECTED_SERVICES_CONGRATS
from telegram.params.select_services_icons import SELECT_SERVICES_ICONS


def get_service_brief_info(service_record: Service,
                           fill_symbols_number: int = None) -> str:
    service_brief_text = (
        f"{SELECT_SERVICES_ICONS.SERVICE_POINT} <b>{service_record.name}</b>\n"
        # For the future
        # f"{SPECIAL_CHARACTERS.FILL_IN_BLANK_SYMBOL * fill_symbols_number}\n"
        f"{" " * 126}"  # Very important for getting same width inline keyboards
        f"{MSG.SERVICE_PRICE}:  {service_record.price} {MSG.CURRENCY_BRIEF}\n"
        f"{MSG.DURATION}:  {service_record.time_duration}\n"
    )
    return service_brief_text


def get_service_brief_info_from_dict(service_info: dict) -> str:
    service_brief_text = (
        f"{MSG.SERVICE_NAME}:  {service_info.get("text")}\n\n"
        f"{MSG.SERVICE_PRICE}:  {service_info.get("price")}  \n"
        f"{MSG.DURATION}:  {service_info.get("duration")}\n")
    return service_brief_text


def get_service_detailed_info(service: Service) -> str:
    service_detailed_text = (
        f"<b>{SELECT_SERVICES_ICONS.SERVICE_POINT} {service.name}</b>\n"
        f"{MSG.SERVICE_PRICE}:  {service.price} {MSG.CURRENCY_BRIEF}\n"
        f"{MSG.SERVICE_DURATION}:  {service.time_duration}\n"
        f"{MSG.SERVICE_DESCRIPTION}:  {service.description}")
    return service_detailed_text


def get_selected_services_summary(services_count: int,
                                  total_cost: float,
                                  total_duration: timedelta) -> str:
    service_summary_text = (
        f"{MSG.SERVICES_TOTAL_COUNT}:  {services_count}\n"
        f"{MSG.SERVICES_TOTAL_COST}:  {total_cost} {MSG.CURRENCY_BRIEF}\n"
        f"{MSG.SERVICES_TOTAL_DURATION}:  {total_duration}")

    return service_summary_text


def get_contacts_text(socials: list,
                      phones: list,
                      addresses: list,
                      phones_international: bool = True) -> str:
    text = ""
    if socials:
        text += f"<b>{MSG.SOCIALS}:</b>\n"

        for social in socials:
            text += f"<a href='{social.url}'>{social.name}</a>\n"
        text += "\n"

    if phones:
        text += f"<b>{MSG.PHONES}:</b>\n"
        if phones_international:
            for phone in phones:
                text += f"{phone.number.international}\n"
        else:
            for phone in phones:
                text += f"{phone.number}\n"
        text += "\n"

    if addresses:
        text += f"<b>{MSG.ADDRESSES}:</b>\n"
        for address in addresses:
            text += f"<a href='{address.url}'>{address.street}</a>\n"
        text += "\n"

    return text


def get_slot_advising_icon(time_loss: timedelta) -> str:
    advised_icon = SPECIAL_CHARACTERS.NO_ACTION_EMPTY_u200B

    if SLOTS_CONFIGS.SHOW_SLOTS_ADVISES:

        if (SLOTS_CONFIGS.MOST_ADVISED_TIME_LOSS_LIMIT
                and time_loss <= timedelta(
                    minutes=SLOTS_CONFIGS.MOST_ADVISED_TIME_LOSS_LIMIT)):
            advised_icon = SLOT_ICONS.MOST_ADVISED_SLOT

        elif (SLOTS_CONFIGS.VERY_ADVISED_TIME_LOSS_LIMIT
              and time_loss <= timedelta(
                    minutes=SLOTS_CONFIGS.VERY_ADVISED_TIME_LOSS_LIMIT)):
            advised_icon = SLOT_ICONS.VERY_ADVISED_SLOT

        elif (SLOTS_CONFIGS.ADVISED_TIME_LOSS_LIMIT
              and time_loss <= timedelta(
                    minutes=SLOTS_CONFIGS.ADVISED_TIME_LOSS_LIMIT)):
            advised_icon = SLOT_ICONS.ADVISED_SLOT

        elif (SLOTS_CONFIGS.UNADVISED_TIME_LOSS_LIMIT
              and time_loss <= timedelta(
                    minutes=SLOTS_CONFIGS.UNADVISED_TIME_LOSS_LIMIT)):
            advised_icon = SLOT_ICONS.UNADVISED_SLOT

        elif (SLOTS_CONFIGS.VERY_UNADVISED_TIME_LOSS_LIMIT
              and time_loss <= timedelta(
                    minutes=SLOTS_CONFIGS.VERY_UNADVISED_TIME_LOSS_LIMIT)):
            advised_icon = SLOT_ICONS.VERY_UNADVISED_SLOT
        else:
            advised_icon = SPECIAL_CHARACTERS.NO_ACTION_EMPTY_u200B

    return advised_icon


def get_slots_advising_brief_note() -> str:
    text = (f"{SLOT_ICONS.ADVISED_SLOT} - {MSG.VERY_ADVISED_SLOTS}   \n"
            f"{SLOT_ICONS.VERY_UNADVISED_SLOT} - {MSG.LESS_ADVISED_SLOTS}")
    return text


def get_slots_advising_explanation():
    text = (f"{SLOTS_RECOMMENDATIONS}:\n\n"
            f"{SLOT_ICONS.MOST_ADVISED_SLOT} - "
            f"{SLOT_ICONS.VERY_ADVISED_SLOT} - "
            f"{SLOT_ICONS.ADVISED_SLOT}  -  "
            f"{BETTER_SLOTS_TO_CHOOSE}\n\n"
            f"{SLOT_ICONS.VERY_UNADVISED_SLOT} - "
            f"{SLOT_ICONS.UNADVISED_SLOT}  -  {CHOOSE_OTHER_SLOTS}")
    return text


def get_summary_services_with_slot(date_text: str,
                                   summary_text: str,
                                   slot_time_start: str,
                                   slot_time_end: str) -> str:
    complete_text = (
        f"{SELECTED_SERVICES_CONGRATS}\n\n"
        f"{CALENDAR_ICONS.CALENDAR} <b>{MSG.SELECTED_DATE}:</b>\n"
        f"{date_text}\n\n"
        f"{summary_text}\n\n"
        f"<b>{MSG.SELECTED_INTERVAL_SLOT}:</b>\n"
        f"{SLOT_ICONS.TIME_SLOT_START_ICON}  "
        f"{slot_time_start}  -  {slot_time_end}  "
        f"{SLOT_ICONS.TIME_SLOT_END_ICON}")
    return complete_text
