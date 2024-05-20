from random import choice

from telegram.params.messages_inserts import MSG
from telegram.params.messages_variants import SERVICE_SELECTED_VARIANTS


def get_service_inl_btn_text(service_record) -> str:
    service_text = (f"{service_record.name} - "
                    f"{service_record.price} {MSG.CURRENCY_BRIEF}  "
                    f"({MSG.DURATION}: {service_record.time_duration})")

    return service_text


def get_service_msg_detailed_text(service) -> str:

    service_detailed_text = (f"{choice(SERVICE_SELECTED_VARIANTS)}:\n\n"
                             f"{MSG.SERVICE_NAME}: {service.name}\n"
                             f"{MSG.SERVICE_PRICE}: {service.price} {MSG.CURRENCY_BRIEF}\n"
                             f"{MSG.SERVICE_DURATION}: {service.time_duration}\n"
                             f"{MSG.SERVICE_DESCRIPTION}: {service.description}")

    return service_detailed_text
