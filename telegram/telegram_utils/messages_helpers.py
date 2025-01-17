from datetime import timedelta

from database.db_models.service_model import (
    Service)
from telegram.config.configs import (
    SLOTS_CONFIGS)
from telegram.params.buttons_common import (
    SPECIAL_CHARACTERS)
from telegram.params.icons_calendar import (
    CALENDAR_ICONS)
from telegram.params.icons_contacts import (
    CONTACTS_ICONS)
from telegram.params.icons_intervals_slots import (
    SLOT_ICONS)
from telegram.params.icons_services import (
    SERVICES_ICONS)
from telegram.params.messages import (
    BETTER_SLOTS_TO_CHOOSE,
    CLICK_ADDRESS_FOR_GEO_MAP,
    SLOTS_RECOMMENDATIONS)
from telegram.params.messages_inserts import (
    MSG)


def get_service_brief_info(
        service_record: Service,
        service_duration: str
) -> str:
    service_brief_text = (
        f"<b>{service_record.name}</b>\n"
        f"{" " * 126}"  # Very important for getting same width inline keyboards
        f"{MSG.SERVICE_PRICE}:  {service_record.price} {MSG.CURRENCY_BRIEF}\n"
        f"{MSG.DURATION}:  {service_duration}\n")
    # f"{MSG.DURATION}:  {str(service_record.time_duration)[:-3]}\n")
    return service_brief_text


def get_service_brief_info_with_master(
        service_record: Service,
        service_duration: str,
        masters_info: str = ""
) -> str:
    service_brief_text = (
        f"<b>{service_record.name}</b>\n"
        f"{" " * 126}"  # Very important for getting same width inline keyboards
        f"{MSG.SERVICE_PRICE}:  {service_record.price} {MSG.CURRENCY_BRIEF}\n"
        f"{MSG.DURATION}:  {service_duration}\n"
        # f"{MSG.DURATION}:  {str(service_record.time_duration)[:-3]}\n"
        f"{MSG.MASTERS}: {masters_info}\n")
    return service_brief_text


def get_service_brief_info_from_dict(service_info: dict) -> str:
    service_brief_text = (
        f"{MSG.SERVICE_NAME}:  {service_info.get("text")}\n\n"
        f"{MSG.SERVICE_PRICE}:  {service_info.get("price")}  \n"
        f"{MSG.DURATION}:  {str(service_info.get("duration"))[:-3]}\n")
    return service_brief_text


def get_service_detailed_info(
        service_obj: Service,
        masters_info: str = "",
        category_name: str = "",
        service_duration: str = ""
) -> str:
    service_detailed_text = (
        f"<b>{SERVICES_ICONS.SERVICE_POINT} {service_obj.name}</b>\n"
        f"{" " * 126}"  # Very important for getting same width inline keyboards
        f"{MSG.SERVICE_PRICE}:  {service_obj.price} {MSG.CURRENCY_BRIEF}\n"
        f"{MSG.SERVICE_DURATION}:  {service_duration}\n"
        f"{MSG.MASTERS}: {masters_info}\n\n"
        # f"{MSG.CATEGORY_NAME}: {category_name}\n\n"
        f"{MSG.SERVICE_DESCRIPTION}:  {service_obj.description}")
    service_detailed_text = service_detailed_text.rstrip(".")
    return service_detailed_text


def get_selected_services_summary(services_count: int,
                                  total_cost: float,
                                  total_duration: str) -> str:
    service_summary_text = (
        f"{MSG.SERVICES_TOTAL_COUNT}:  {services_count}\n"
        f"{MSG.SERVICES_TOTAL_COST}:  {total_cost} {MSG.CURRENCY_BRIEF}\n"
        f"{MSG.SERVICES_TOTAL_DURATION}:  {total_duration}")

    return service_summary_text


def get_contacts_text(socials: list = None,
                      phones: list = None,
                      addresses: list = None,
                      phones_international: bool = True) -> str | None:
    text = ""
    if socials:
        text += (f"{CONTACTS_ICONS.SOCIALS_ICON}  "
                 f"<b>{MSG.SOCIALS}:</b>\n\n")
        for social in socials:
            if social.url:
                text += (f"<a href='{social.url}'>{social.name}:  "
                         f"<b>{social.social_username}</b></a>\n\n")
            else:
                text += (f"{social.name}:  "
                         f"<code>{social.social_username}</code>\n\n")

    if phones:
        text += (f"{CONTACTS_ICONS.PHONES_ICON}  "
                 f"<b>{MSG.PHONES}:</b>\n\n")
        if phones_international:
            for phone in phones:
                text += f"{phone.number.international}\n\n"
        else:
            for phone in phones:
                text += f"{phone.number}\n\n"

    if addresses:
        text += (f"{CONTACTS_ICONS.LOCATION_ICON}  "
                 f"<b>{MSG.ADDRESSES}:</b>\n\n")
        for address in addresses:
            if address.url:
                text += (f"<b><a href='{address.url}'>"
                         f"{address.street}</a></b>\n\n")
            else:
                text += f"<b>{address.street}</b>\n\n"

    return text


def get_addresses_for_maps_text(addresses: list = None) -> str | None:
    text = ""
    if addresses:
        if all(address.url for address in addresses):
            text += (f"{CONTACTS_ICONS.CAR_ICON}  "
                     f"{CLICK_ADDRESS_FOR_GEO_MAP}:\n\n")
        else:
            text += (f"{CONTACTS_ICONS.LOCATION_ICON}  "
                     f"<b>{MSG.ADDRESSES}:</b>\n\n")

        for address in addresses:
            if address.url:
                text += (f"{CONTACTS_ICONS.DESTINATION_ICON}  "
                         f"<b><a href='{address.url}'>"
                         f"{address.street}</a></b>\n\n")
            else:
                text += (f"{CONTACTS_ICONS.DESTINATION_ICON}  "
                         f"<b>{address.street}</b>\n\n")

    return text


def get_slot_advising_icon(time_loss: timedelta) -> str:
    advised_icon = SPECIAL_CHARACTERS.NO_ACTION_EMPTY_u200B

    if SLOTS_CONFIGS.SHOW_SLOTS_ADVISES_ICONS:

        if (SLOTS_CONFIGS.POINTS_5_TIME_LOSS_LIMIT
                and time_loss <= timedelta(
                    minutes=SLOTS_CONFIGS.POINTS_5_TIME_LOSS_LIMIT)):
            advised_icon = SLOT_ICONS.MAX_ADVISED_SLOT

        elif (SLOTS_CONFIGS.POINTS_4_TIME_LOSS_LIMIT
              and time_loss <= timedelta(
                    minutes=SLOTS_CONFIGS.POINTS_4_TIME_LOSS_LIMIT)):
            advised_icon = SLOT_ICONS.HIGHLY_ADVISED_SLOT

        elif (SLOTS_CONFIGS.POINTS_3_TIME_LOSS_LIMIT
              and time_loss <= timedelta(
                    minutes=SLOTS_CONFIGS.POINTS_3_TIME_LOSS_LIMIT)):
            advised_icon = SLOT_ICONS.ADVISED_SLOT

        elif (SLOTS_CONFIGS.POINTS_2_TIME_LOSS_LIMIT
              and time_loss <= timedelta(
                    minutes=SLOTS_CONFIGS.POINTS_2_TIME_LOSS_LIMIT)):
            advised_icon = SLOT_ICONS.STANDARD_SLOT

        elif (SLOTS_CONFIGS.POINTS_1_TIME_LOSS_LIMIT
              and time_loss <= timedelta(
                    minutes=SLOTS_CONFIGS.POINTS_1_TIME_LOSS_LIMIT)):
            advised_icon = SLOT_ICONS.BASIC_SLOT
        else:
            advised_icon = SPECIAL_CHARACTERS.NO_ACTION_EMPTY_u200B

    return advised_icon


def get_slots_advising_brief_note() -> str:
    text = (f"{BETTER_SLOTS_TO_CHOOSE}:  "
            f"{SLOT_ICONS.BASIC_SLOT} - {SLOT_ICONS.MAX_ADVISED_SLOT}")
    return text


def get_slots_advising_explanation():
    text = (f"{BETTER_SLOTS_TO_CHOOSE}\n\n"
            f"{SLOTS_RECOMMENDATIONS}:\n"
            f"{SLOT_ICONS.MAX_ADVISED_SLOT} - {MSG.MAX_ADVISED_SLOTS}\n"
            f"{SLOT_ICONS.HIGHLY_ADVISED_SLOT} - {MSG.HIGHLY_ADVISED_SLOTS}\n"
            f"{SLOT_ICONS.ADVISED_SLOT} - {MSG.ADVISED_SLOT}\n"
            f"{SLOT_ICONS.STANDARD_SLOT} - {MSG.STANDARD_SLOT}\n"
            f"{SLOT_ICONS.BASIC_SLOT} - {MSG.BASIC_SLOTS}\n\n")
    return text


def get_summary_services_with_slot(congratulation_text: str,
                                   date_text: str,
                                   summary_text: str,
                                   slot_time_start: str,
                                   slot_time_end: str) -> str:
    complete_text = (
        f"{congratulation_text}\n\n"
        f"{CALENDAR_ICONS.CALENDAR} <b>{MSG.SELECTED_DATE}:</b>\n"
        f"{date_text}\n\n"
        f"{summary_text}\n\n"
        f"<b>{MSG.SELECTED_INTERVAL_SLOT}:</b>\n"
        f"{SLOT_ICONS.TIME_SLOT_START_ICON}  "
        f"{slot_time_start}  -  {slot_time_end}  "
        f"{SLOT_ICONS.TIME_SLOT_END_ICON}")
    return complete_text


def get_reservation_detailed_info(reservation_weekday: str,
                                  reservation_date: str,
                                  reservation_time_start: str,
                                  reservation_time_end: str,
                                  selected_services_duration: str,
                                  selected_services_cost: float,
                                  reserved_services_names: str,
                                  reserved_masters_names: str
                                  ) -> str:
    text = (f"{reservation_date} {reservation_weekday}\n"
            f"{MSG.TIME}: {reservation_time_start} - {reservation_time_end}\n\n"
            f"{MSG.DURATION}: {selected_services_duration}\n"
            f"{MSG.COST}: {selected_services_cost} {MSG.CURRENCY_BRIEF}\n"
            f"{MSG.MASTERS}: {reserved_masters_names}\n\n"
            f"{MSG.SERVICES}: {reserved_services_names}")
    text = text.rstrip(".")

    # TG callback query alert message limit max 200 symbols
    text = text[0:197] + "..." if len(text) > 200 else text
    return text
