from aiogram import Router, F
from aiogram.types import Message

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from telegram.filters.chat_types_filter import IsAdmin
from telegram.params.buttons_main_menu import MAIN_MANU_ADMIN_PARAMS as MAIN_PARAMS
from telegram.keyboard_reply.admin_main_menu_kbd import get_admin_main_menu_kbd
from telegram.keyboard_reply.admin_add_services_kbd import get_keyboard, get_change_service_keyboard
from telegram.params.buttons_add_services import BUTTONS_ADD_SERVICES
from telegram.params.buttons_change_services import BUTTONS_CHANGE_SERVICES

from telegram.params.messages import (
    ADD_DESCRIPTION_SERVICE,
    ADD_NAME_SERVICE,
    ADD_PRICE_SERVICE
)

from database.db_queries.admin_queries import add_services

from utilities.validate import is_float

services_admin_btn_router = Router(name=__name__)
services_admin_btn_router.message.filter(IsAdmin())


class Services(StatesGroup):
    name = State()
    description = State()
    price = State()
    decision = State()
    change = State()


@services_admin_btn_router.message(F.text == MAIN_PARAMS.ADD_SERVICES)
async def add_name_service(message: Message, state: FSMContext):
    await message.answer(text=ADD_NAME_SERVICE)
    await state.set_state(Services.name)


@services_admin_btn_router.message(StateFilter(Services.name))
async def add_description_service(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer(text=ADD_DESCRIPTION_SERVICE)
    await state.set_state(Services.description)


@services_admin_btn_router.message(StateFilter(Services.description))
async def add_price_service(message: Message, state: FSMContext):
    await state.update_data(description=message.text)

    await message.answer(text=ADD_PRICE_SERVICE)
    await state.set_state(Services.price)


@services_admin_btn_router.message(StateFilter(Services.price))
async def add_price(message: Message, state: FSMContext):
    if is_float(data=message.text):
        await state.update_data(price=message.text)

        return await preview_service(message=message, state=state)

    else:
        await message.answer(text='Enter a number ')
        await state.set_state(Services.price)


async def preview_service(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.answer(text=f'Name: {data["name"]}\n'
                              f'Description: {data["description"]}\n'
                              f'Price: {data["price"]}',
                         reply_markup=get_keyboard()
                         )

    await state.set_state(Services.decision)


@services_admin_btn_router.message(StateFilter(Services.decision))
async def get_decision(message: Message, state: FSMContext):
    if message.text == BUTTONS_ADD_SERVICES.ADD:
        data = await state.get_data()

        add_services(data)

        await message.answer(text=f'Service added.', reply_markup=get_admin_main_menu_kbd())
        await state.clear()

    elif message.text == BUTTONS_ADD_SERVICES.REMOVE_SERVICE:
        await state.clear()
        await message.answer(text=f'Service removed.', reply_markup=get_admin_main_menu_kbd())

    else:
        await message.answer(text='Выбери что ты хочешь изменить', reply_markup=get_change_service_keyboard())
        await state.set_state(Services.change)


@services_admin_btn_router.message(StateFilter(Services.change))
async def change_service(message: Message, state: FSMContext):
    match message.text:
        case BUTTONS_CHANGE_SERVICES.NAME:
            await state.update_data(change=message.text)

            await message.answer(text='Введите новое название услуги')
            await state.set_state(Services.change)

        case BUTTONS_CHANGE_SERVICES.DESCRIPTION:
            await state.update_data(change=message.text)

            await message.answer(text='Введите новое название описания')
            await state.set_state(Services.change)

        case BUTTONS_CHANGE_SERVICES.PRICE:
            await state.update_data(change=message.text)

            await message.answer(text='Введите новую цену')
            await state.set_state(Services.change)

        case _:
            data = await state.get_data()
            params_change = data.get('change')

            match params_change:
                case BUTTONS_CHANGE_SERVICES.NAME:
                    await state.update_data(name=message.text)
                    return await preview_service(message=message, state=state)

                case BUTTONS_CHANGE_SERVICES.DESCRIPTION:
                    await state.update_data(description=message.text)
                    return await preview_service(message=message, state=state)

                case BUTTONS_CHANGE_SERVICES.PRICE:
                    return await add_price(message=message, state=state)

