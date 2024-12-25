from database.db_models.work_time_model import WorkTime


def get_info_about_reserved_slot(slot: WorkTime):
    user = slot.work_time_clients[0]
    services = {
        'name': [],
        'price': []
    }

    for service in slot.work_time_services:
        services['name'].append(service.name)
        services['price'].append(service.price)

    client_info = (
        f'<a href="https://t.me/{user.username}">{user.get_full_name}</a>'
        if user.username else user.get_full_name
    )

    text = (
        f'Время: {slot.time_start.strftime("%H:%M")} - {slot.time_end.strftime("%H:%M")}\n'
        f'Клиент: {client_info}\n'
        f'Номер телефона: <a href="{user.phone_number}">{user.phone_number if user.phone_number is not None else ''}</a>\n'
        f'Услуги: {", ".join(services.get('name'))}\n'
        f'Цена: {sum(services.get('price'))}')

    return text
