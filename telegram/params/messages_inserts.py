from dataclasses import dataclass


@dataclass
class MSG:
    DATE: str = "Дата"
    TIME: str = "Время"
    NAME: str = "Имя"
    PRICE: str = "Цена"
    DURATION: str = "Общее время"
    COST: str = "Цена"
    DESCRIPTION: str = "Описание"
    COUNT: str = "Количество"

    MASTERS: str = "Мастера"
    SERVICES: str = "Услуги"

    SERVICES_TOTAL_COST: str = "💰 Общая цена"
    SERVICES_TOTAL_DURATION: str = "🕑 Общее время"
    SERVICES_TOTAL_COUNT: str = "✂️ Всего услуг"

    CURRENCY_BRIEF: str = "руб"

    SERVICE_NAME: str = "Услуга"
    SERVICE_PRICE: str = "Цена"
    SERVICE_DURATION: str = "Время"
    SERVICE_DESCRIPTION: str = "Описание"

    CATEGORY_NAME: str = "Категория"

    SOCIALS: str = "🌐 Социальные сети"
    PHONES: str = "📞 Телефоны"
    ADDRESSES: str = "📍 Адресы"

    SELECTED_DATE: str = "Выбранная дата"
    SELECTED_INTERVAL_SLOT: str = "Выбранное время"

    SLOTS_RECOMMENDATIONS: str = "Рекомендации"
    MAX_ADVISED_SLOTS: str = "Максимальный"
    HIGHLY_ADVISED_SLOTS: str = "Высокий"
    ADVISED_SLOT: str = "Стандартный"
    STANDARD_SLOT: str = "Обычный"
    BASIC_SLOTS: str = "Базовый"
