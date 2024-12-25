from aiogram import Router, F
from aiogram.types import Message

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from telegram.filters.chat_types_filter import IsAdmin
from telegram.keyboard_inline.services_change_select_inl_kbd import services_select_inl_kbd
from telegram.keyboard_inline.services_time_duration_add_inl_kbd import (
    add_hours_time_duration_services_inl_kbd,
    add_minutes_time_duration_services_inl_kbd
)

from telegram.keyboard_reply.admin_services_action_kbd import get_services_action_kbd
from telegram.params.buttons_main_menu import MAIN_MANU_ADMIN_PARAMS as MAIN_PARAMS
from telegram.keyboard_reply.admin_main_menu_kbd import get_admin_main_menu_kbd
from telegram.keyboard_reply.admin_add_services_kbd import get_keyboard, get_change_service_keyboard
from telegram.params.buttons_add_services import BUTTONS_ADD_SERVICES
from telegram.params.buttons_change_services import BUTTONS_CHANGE_SERVICES
from telegram.params.button_services_action import BUTTON_SERVICES_ACTION

from telegram.params.messages import (
    ADD_DESCRIPTION_SERVICE,
    ADD_NAME_SERVICE,
    ADD_PRICE_SERVICE,
    CHOOSE_AN_ACTION,
)

from telegram.params.services_btn_admin_message import (
    AddTimeDurationServiceMessage,
    AddPriceMessage,
    GetDecision,
    ChangeService
)

from database.db_queries.admin_queries import add_services
from database.db_queries.user_queries import get_services_list

from utilities.service_time_format import get_time_duration_for_admin_preview
from utilities.validate import is_float

services_admin_btn_router = Router(name=__name__)
services_admin_btn_router.message.filter(IsAdmin())


class Services(StatesGroup):
    name = State()
    description = State()
    price = State()
    decision = State()
    change = State()
    id_service = State()
    duration_hours = State()
    duration_minutes = State()
    duration_entered = State()
    messages_id = State()


@services_admin_btn_router.message(F.text == MAIN_PARAMS.SERVICES)
async def get_services_action(message: Message):
    await message.answer(text=CHOOSE_AN_ACTION, reply_markup=get_services_action_kbd())


@services_admin_btn_router.message(F.text == BUTTON_SERVICES_ACTION.ADD)
async def add_name_service(message: Message, state: FSMContext):
    await message.answer(text=ADD_NAME_SERVICE)
    await state.set_state(Services.name)


@services_admin_btn_router.message(StateFilter(Services.name))
async def add_description_service(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer(text=ADD_DESCRIPTION_SERVICE)
    await state.set_state(Services.description)


@services_admin_btn_router.message(StateFilter(Services.description))
async def add_time_duration_service(message: Message, state: FSMContext, description=None):
    if description is None:
        await state.update_data(description=message.text)

    await message.answer(text=AddTimeDurationServiceMessage.SELECT_DURATION)

    await message.answer(
        text=AddTimeDurationServiceMessage.HOURS,
        reply_markup=add_hours_time_duration_services_inl_kbd()
    )
    await message.answer(
        text=AddTimeDurationServiceMessage.MINUTES,
        reply_markup=add_minutes_time_duration_services_inl_kbd()
    )

    await state.set_state(Services.duration_entered)


async def add_price_service(message: Message, state: FSMContext):
    await message.answer(text=ADD_PRICE_SERVICE)
    await state.set_state(Services.price)


@services_admin_btn_router.message(StateFilter(Services.price))
async def add_price(message: Message, state: FSMContext):
    if is_float(data=message.text):
        await state.update_data(price=message.text)

        return await preview_service(message=message, state=state)

    else:
        await message.answer(text=AddPriceMessage.ENTER_NUMBER)
        await state.set_state(Services.price)


async def preview_service(message: Message, state: FSMContext, cb_data=None):
    if cb_data:
        await state.update_data(
            name=cb_data.get('name'),
            description=cb_data.get('description'),
            price=cb_data.get('price'),
            id_service=cb_data.get('id'),
            duration_hours=cb_data.get('hours'),
            duration_minutes=cb_data.get('minutes'),
            duration_entered=cb_data.get('duration_entered')
        )

    data = await state.get_data()

    time_duration = get_time_duration_for_admin_preview(hours=data['duration_hours'], minutes=data['duration_minutes'])

    await message.answer(text=f'Name: {data["name"]}\n'
                              f'Description: {data["description"]}\n'
                              f'Time duration: {time_duration}\n'
                              f'Price: {data["price"]}\n',
                         reply_markup=get_keyboard()
                         )

    await state.set_state(Services.decision)


@services_admin_btn_router.message(StateFilter(Services.decision))
async def get_decision(message: Message, state: FSMContext):
    if message.text == BUTTONS_ADD_SERVICES.ADD:
        data = await state.get_data()
        user_telegram_id = message.from_user.id

        add_services(data, user_telegram_id=user_telegram_id)

        await message.answer(text=GetDecision.ADD, reply_markup=get_admin_main_menu_kbd())
        await state.clear()

    elif message.text == BUTTONS_ADD_SERVICES.REMOVE_SERVICE:
        await state.clear()
        await message.answer(text=GetDecision.REMOVE, reply_markup=get_admin_main_menu_kbd())

    elif message.text == BUTTONS_ADD_SERVICES.CHANGE_SERVICE:
        await message.answer(text=GetDecision.CHANGE, reply_markup=get_change_service_keyboard())
        await state.set_state(Services.change)


@services_admin_btn_router.message(StateFilter(Services.change))
async def change_service(message: Message, state: FSMContext):
    match message.text:
        case BUTTONS_CHANGE_SERVICES.NAME:
            await state.update_data(change=message.text)

            await message.answer(text=ChangeService.NAME)
            return await state.set_state(Services.change)

        case BUTTONS_CHANGE_SERVICES.DESCRIPTION:
            await state.update_data(change=message.text)

            await message.answer(text=ChangeService.DESCRIPTION)
            return await state.set_state(Services.change)

        case BUTTONS_CHANGE_SERVICES.PRICE:
            await state.update_data(change=message.text)

            await message.answer(text=ChangeService.PRICE)
            return await state.set_state(Services.change)

        case BUTTONS_CHANGE_SERVICES.DURATION:
            await state.update_data(change=message.text)

    data = await state.get_data()
    change = data.get('change')

    if change:
        match change:
            case BUTTONS_CHANGE_SERVICES.NAME:
                await state.update_data(name=message.text)
                return await preview_service(message=message, state=state)

            case BUTTONS_CHANGE_SERVICES.DESCRIPTION:
                await state.update_data(description=message.text)
                return await preview_service(message=message, state=state)

            case BUTTONS_CHANGE_SERVICES.PRICE:
                return await add_price(message=message, state=state)

            case BUTTONS_CHANGE_SERVICES.DURATION:
                await state.update_data(
                    duration_hours=None,
                    duration_minutes=None
                )

                return await add_time_duration_service(description=True, message=message, state=state)


@services_admin_btn_router.message(F.text == BUTTON_SERVICES_ACTION.CHANGE)
@services_admin_btn_router.message(F.text == BUTTON_SERVICES_ACTION.Remove)
async def services_change_or_remove(message: Message, state: FSMContext):
    data = get_services_list()
    messages_id = []

    if message.text == BUTTON_SERVICES_ACTION.Remove:
        for service in data:
            total_seconds = service.time_duration.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)

            time_duration = get_time_duration_for_admin_preview(
                hours=hours,
                minutes=minutes
            )

            massage = await message.answer(text=f'Name: {service.name}\n'
                                                f'Description: {service.description}\n'
                                                f'Time duration: {time_duration}\n'
                                                f'Price: {service.price}\n',
                                           reply_markup=services_select_inl_kbd(action=True, id_service=service.id)
                                           )
            messages_id.append(massage.message_id)

        return await state.update_data(messages_id=messages_id)

    for service in data:
        total_seconds = service.time_duration.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)

        time_duration = get_time_duration_for_admin_preview(
            hours=hours,
            minutes=minutes
        )

        message = await message.answer(text=f'Name: {service.name}\n'
                                            f'Description: {service.description}\n'
                                            f'Time duration: {time_duration}\n'
                                            f'Price: {service.price}\n',
                                       reply_markup=services_select_inl_kbd(id_service=service.id, quantity=len(data))
                                       )

        messages_id.append(message.message_id)

    return await state.update_data(messages_id=messages_id)
