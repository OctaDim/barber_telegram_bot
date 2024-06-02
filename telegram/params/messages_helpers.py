from random import choice

from database.db_models.services_model import Services

from telegram.params.messages_inserts import MSG
from telegram.params.messages_variants import SERVICE_SELECTED_VARIANTS


def get_service_brief_info(service_record: Services) -> str:
    service_brief_text = (f"{service_record.name} - "
                          f"{service_record.price} {MSG.CURRENCY_BRIEF}  "
                          f"({MSG.DURATION}: {service_record.time_duration})")

    return service_brief_text


def get_service_detailed_info(service: Services) -> str:
    service_detailed_text = (f"<b>{choice(SERVICE_SELECTED_VARIANTS)}:</b>\n\n"
                             f"<b>{MSG.SERVICE_NAME}:</b> "
                             f"{service.name}\n"
                             f"<b>{MSG.SERVICE_PRICE}:</b> "
                             f"{service.price} {MSG.CURRENCY_BRIEF}\n"
                             f"<b>{MSG.SERVICE_DURATION}:</b> "
                             f"{service.time_duration}\n"
                             f"<b>{MSG.SERVICE_DESCRIPTION}:</b> {service.description}")

    return service_detailed_text
