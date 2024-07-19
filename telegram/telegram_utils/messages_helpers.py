from random import randrange
from datetime import timedelta

from database.db_models.services_model import Services

from telegram.params.messages_inserts import MSG
from telegram.params.messages_variants import SERVICES_SALUTES_VARIANTS
from telegram.params.select_services_icons import SELECT_SERVICES_ICONS


def get_service_brief_info_from_record(service_record: Services) -> str:
    service_brief_text = (
        f"{MSG.SERVICE_NAME}:  {service_record.name}\n\n"
        f"{MSG.SERVICE_PRICE}:  {service_record.price} {MSG.CURRENCY_BRIEF}  \n"
        f"{MSG.DURATION}:  {service_record.time_duration}")
    return service_brief_text


def get_service_brief_info_from_dict(service_info: dict) -> str:
    service_brief_text = (
        f"{MSG.SERVICE_NAME}:  {service_info.get("text")}\n\n"
        f"{MSG.SERVICE_PRICE}:  {service_info.get("price")}  \n"
        f"{MSG.DURATION}:  {service_info.get("duration")}\n")
    return service_brief_text


def get_service_detailed_info(service: Services) -> str:
    service_detailed_text = (
        f"{SELECT_SERVICES_ICONS.MARKER} <b>{service.name}</b>\n\n"
        f"<b>{MSG.SERVICE_PRICE}:</b>  {service.price} {MSG.CURRENCY_BRIEF}\n"
        f"<b>{MSG.SERVICE_DURATION}:</b>  {service.time_duration}\n"
        f"<b>{MSG.SERVICE_DESCRIPTION}:</b>  {service.description}")
    return service_detailed_text


def get_selected_services_summary(services_count: int,
                                  total_cost: float,
                                  total_duration: timedelta,
                                  salute_flag: bool = False) -> str:
    if salute_flag:
        all_salutes_number = len(SERVICES_SALUTES_VARIANTS)
        random_salute_index = randrange(0, all_salutes_number) - 1
        rand_enroll_srcs_salute = SERVICES_SALUTES_VARIANTS[random_salute_index]
        rand_enroll_srcs_salute = f"<b>{rand_enroll_srcs_salute}</b>"
    else:
        rand_enroll_srcs_salute = ""

    service_summary_text = (
        f"{rand_enroll_srcs_salute}\n\n"
        f"{MSG.SERVICES_TOTAL_COUNT}:  {services_count}\n"
        f"{MSG.SERVICES_TOTAL_COST}:  {total_cost} {MSG.CURRENCY_BRIEF}\n"
        f"{MSG.SERVICES_TOTAL_DURATION}:  {total_duration}")

    return service_summary_text
