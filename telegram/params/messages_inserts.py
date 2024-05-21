from dataclasses import dataclass


@dataclass
class MSG:
    NAME: str = "Name"
    DESCRIPTION: str = "Description"
    PRICE: str = "Price"
    DURATION: str = "Duration"

    TOTAL_COST: str = "Total cost"
    TOTAL_DURATION: str = "Total duration"
    TOTAL_COUNT: str = "Total count"

    CURRENCY_BRIEF: str = "byn"

    SERVICE_NAME: str = "Service name"
    SERVICE_DESCRIPTION: str = "Description"
    SERVICE_PRICE: str = "Service price"
    SERVICE_DURATION: str = "Service duration"
