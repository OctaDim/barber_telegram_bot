from datetime import timedelta

from random import randrange

from database.db_models.services_model import Services

from telegram.params.messages_inserts import MSG
from telegram.params.messages_variants import SERVICE_SALUTATIONS_VARIANTS
from telegram.params.select_services_icons import SELECT_SERVICES_ICONS


def get_service_brief_info_from_record(service_record: Services) -> str:
    service_brief_text = (
        f"<b>{MSG.SERVICE_NAME}: {service_record.name}\n</b>"
        f"{MSG.SERVICE_PRICE}: {service_record.price} {MSG.CURRENCY_BRIEF}  \n"
        f"{MSG.DURATION}: {service_record.time_duration}")
    return service_brief_text


def get_service_brief_info_from_dict(service_info: dict) -> str:
    service_brief_text = (
        f"{MSG.SERVICE_NAME}: {service_info.get("text")}\n"
        f"{MSG.SERVICE_PRICE}: {service_info.get("price")}  \n"
        f"{MSG.DURATION}: {service_info.get("duration")}\n")
    return service_brief_text


def get_service_detailed_info(service: Services) -> str:
    service_detailed_text = (
        f"\n{SELECT_SERVICES_ICONS.MARKER} <b>{service.name}</b>\n"
        f"{MSG.SERVICE_PRICE}: {service.price} {MSG.CURRENCY_BRIEF}\n"
        f"{MSG.SERVICE_DURATION}: {service.time_duration}\n"
        f"{MSG.SERVICE_DESCRIPTION}: {service.description}")
    return service_detailed_text


def get_selected_services_summary(services_count: int,
                                  total_cost: float,
                                  total_duration: timedelta,
                                  salutation_flag: bool = False) -> str:
    if salutation_flag:
        random_salutation = f"<b>{SERVICE_SALUTATIONS_VARIANTS[
            randrange(0, len(SERVICE_SALUTATIONS_VARIANTS) - 1)]}</b>"
    else:
        random_salutation = ""

    service_summary_text = (
        f"{random_salutation}\n\n"
        f"{MSG.SERVICES_TOTAL_COUNT} {services_count}\n"
        f"{MSG.SERVICES_TOTAL_COST} {total_cost} {MSG.CURRENCY_BRIEF}\n"
        f"{MSG.SERVICES_TOTAL_DURATION} {total_duration}")
    return service_summary_text
