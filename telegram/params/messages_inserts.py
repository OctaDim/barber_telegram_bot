from dataclasses import dataclass


@dataclass
class MSG:
    NAME: str = "Name"
    PRICE: str = "Price"
    DURATION: str = "Duration"
    DESCRIPTION: str = "Description"

    TOTAL_COST: str = "Total cost"
    TOTAL_DURATION: str = "Total duration"
    TOTAL_COUNT: str = "Total count"

    CURRENCY_BRIEF: str = "byn"

    SERVICE_NAME: str = "Name"
    SERVICE_PRICE: str = "Price"
    SERVICE_DURATION: str = "Duration"
    SERVICE_DESCRIPTION: str = "Description"
