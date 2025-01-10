
from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from database.db_queries.all_categories_by_master_query import get_all_categories_by_master_query
from database.db_queries.category_update_data_query import category_update_data_query
from database.db_queries.create_category_query import create_category_query
from telegram.filters.chat_types_filter import IsAdmin
from telegram.keyboard_inline.admin_categories_get_categories_for_cahnge_inl_kbd import get_category_for_change_inl_kbd
from telegram.keyboard_inline.admin_category_get_category_for_remove_inl_kbd import get_category_for_remove_inl_kbd
from telegram.keyboard_reply.admin_categories_get_action_by_categories_kbd import get_action_by_categories_replay_kbd

from telegram.keyboard_reply.admin_categories_get_choose_service_or_categories import \
    get_choose_service_or_categories_replay_kbd
from telegram.keyboard_reply.admin_main_menu_kbd import get_admin_main_menu_kbd

from telegram.params.admin_categories_message import SELECT_ACTION, ADD_NAME_CATEGORIES, SELECT_CATEGORY, \
    NOT_HAVE_CATEGORIES
from telegram.params.button_admin_panel_or_main_menu import ButtonAdminPanelOrMainMenu
from telegram.params.buttons_admin_categories import CHOOSE_SERVICE_OR_CATEGORIES, ADMIN_CATEGORIES_ACTION
from telegram.params.buttons_main_menu import MAIN_MANU_ADMIN_PARAMS

admin_categories_btn_router = Router(name=__name__)
admin_categories_btn_router.message.filter(IsAdmin())


class AdminCategories(StatesGroup):
    name = State()
    category_id = State()


@admin_categories_btn_router.message(F.text == MAIN_MANU_ADMIN_PARAMS.CATEGORIES)
async def get_choose_service_or_categories(message: Message):
    await message.answer(
        text=SELECT_ACTION,
        reply_markup=get_choose_service_or_categories_replay_kbd())


@admin_categories_btn_router.message(F.text == CHOOSE_SERVICE_OR_CATEGORIES.CATEGORIES)
async def get_action_by_categories(message: Message):
    await message.answer(
        text=SELECT_ACTION,
        reply_markup=get_action_by_categories_replay_kbd()
    )


@admin_categories_btn_router.message(F.text == ADMIN_CATEGORIES_ACTION.ADD)
async def add_name_categories(message: Message, state: FSMContext):
    await message.answer(
        text=ADD_NAME_CATEGORIES,
        reply_markup=get_admin_main_menu_kbd()
    )

    await state.set_state(AdminCategories.name)


@admin_categories_btn_router.message(StateFilter(AdminCategories.name))
async def create_new_category(message: Message, state: FSMContext):
    await state.set_state(None)

    await message.answer(
        text=ButtonAdminPanelOrMainMenu.ADMIN_PANEL,
        reply_markup=get_admin_main_menu_kbd()
    )
    state_data = await state.get_data()
    category_id = state_data.get('category_id')

    if category_id:
        category_update_data_query(
            category_id=category_id,
            name=message.text.capitalize())

        return

    create_category_query(
        name=message.text.capitalize(),
        telegram_id=message.from_user.id
    )

    await state.clear()


@admin_categories_btn_router.message(F.text == ADMIN_CATEGORIES_ACTION.CHANGE)
async def get_categories_for_change(message: Message, state: FSMContext):
    messages_id = []

    categories = get_all_categories_by_master_query(
        telegram_id=message.from_user.id)

    if len(categories) == 0:
        await message.answer(
            text=NOT_HAVE_CATEGORIES,
            reply_markup=get_action_by_categories_replay_kbd()
        )
        return

    await message.answer(
        text=SELECT_CATEGORY,
        reply_markup=get_admin_main_menu_kbd()
    )

    for category in categories:
        message = await message.answer(
            text=category.name.capitalize(),
            reply_markup=get_category_for_change_inl_kbd(
                category_id=category.id
            )
        )

        messages_id.append(message.message_id)

    await state.update_data(messages_id=messages_id)


async def change_category(message: Message, state: FSMContext):
    await message.answer(text=ADD_NAME_CATEGORIES)

    await state.set_state(AdminCategories.name)


@admin_categories_btn_router.message(F.text == ADMIN_CATEGORIES_ACTION.REMOVE)
async def get_categories_for_remove(message: Message, state: FSMContext):
    messages_id = []

    categories = get_all_categories_by_master_query(
        telegram_id=message.from_user.id)

    if len(categories) == 0:
        await message.answer(
            text=NOT_HAVE_CATEGORIES,
            reply_markup=get_action_by_categories_replay_kbd()
        )
        return

    await message.answer(
        text=SELECT_CATEGORY,
        reply_markup=get_admin_main_menu_kbd()
    )

    for category in categories:
        message = await message.answer(
            text=category.name.capitalize(),
            reply_markup=get_category_for_remove_inl_kbd(
                category_id=category.id
            )
        )

        messages_id.append(message.message_id)

    await state.update_data(messages_id=messages_id)