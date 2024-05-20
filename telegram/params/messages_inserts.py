from dataclasses import dataclass


@dataclass
class MSG:
    NAME = "Name"
    DESCRIPTION = "Description"
    PRICE = "Price"
    DURATION = "Duration"

    TOTAL_COST = "Total cost"
    TOTAL_DURATION = "Total duration"
    TOTAL_COUNT = "Total count"

    CURRENCY_BRIEF = "byn"

    SERVICE_NAME = "Service name"
    SERVICE_DESCRIPTION = "Description"
    SERVICE_PRICE = "Service price"
    SERVICE_DURATION = "Service duration"
