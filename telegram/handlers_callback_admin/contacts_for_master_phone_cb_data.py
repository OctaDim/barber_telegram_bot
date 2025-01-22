from aiogram import Router, Bot

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_queries.check_phone_in_db_query import check_phone_in_db
from database.db_queries.create_new_phone_for_master_query import create_phone_for_master
from database.db_queries.get_all_phone_by_master import get_all_phone_by_masters
from database.db_queries.remove_phone_by_phone_id_query import remove_phone_by_phone_id
from database.db_queries.update_phone_by_phone_id_query import update_phone_by_phone_id
from telegram.handlers_admin.contacts_admin_phone_btn_admin import ContactsAdminPhone
from telegram.keyboard_inline.contacts_for_master_get_action_by_phone import AddNewPhoneCbData, ChangePhoneCbData, \
    RemovePhoneCbData
from telegram.keyboard_inline.contacts_for_master_get_all_phone_for_changes_inl_kbd import \
    get_all_phone_for_changes_inl_kbd, PhoneForChangesCbData
from telegram.keyboard_inline.contacts_for_master_get_all_phone_for_delete import get_all_phone_for_delete_inl_kbd, \
    PhoneForDeleteCbData

from telegram.keyboard_inline.contacts_for_master_preview_phone import ChangePreviewPhoneCbData, \
    ConfirmPreviewPhoneCbData
from telegram.keyboard_reply.admin_main_menu_kbd import get_admin_main_menu_kbd
from telegram.params.button_admin_panel_or_main_menu import ButtonAdminPanelOrMainMenu
from telegram.params.button_social_networks import PreviewPhone

from telegram.params.contacts_for_master_cb_data_message import ADD_PHONE, PHONE_IN_DB_ERROR
from telegram.params.timetable_cb_data_message import SUCCESSFULLY, NOT_CONTACTS_ERROR, NOT_PHONES_ERROR

contacts_for_master_phone_master_cb_query = Router(name=__name__)


@contacts_for_master_phone_master_cb_query.callback_query(ChangePreviewPhoneCbData.filter())
@contacts_for_master_phone_master_cb_query.callback_query(AddNewPhoneCbData.filter())
async def select_add_new_phone(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot,
):
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=ADD_PHONE,
        reply_markup=None
    )

    await state.set_state(ContactsAdminPhone.phone)


@contacts_for_master_phone_master_cb_query.callback_query(ConfirmPreviewPhoneCbData.filter())
async def add_new_phone_master(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    state_data = await state.get_data()

    phone_obj = check_phone_in_db(phone=state_data.get('phone'))

    if phone_obj:
        await callback_query.answer(text=PHONE_IN_DB_ERROR, show_alert=True)
        return

    await callback_query.answer(text=SUCCESSFULLY, show_alert=True)
    if state_data.get('phone_id'):
        update_phone_by_phone_id(
            phone_id=state_data.get('phone_id'),
            phone=state_data.get('phone')
        )

    else:
        create_phone_for_master(
            telegram_id=callback_query.from_user.id,
            phone=state_data.get('phone')
        )

    await bot.delete_message(
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id
    )

    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=ButtonAdminPanelOrMainMenu.ADMIN_PANEL,
        reply_markup=get_admin_main_menu_kbd()
    )

    await state.clear()


@contacts_for_master_phone_master_cb_query.callback_query(ChangePhoneCbData.filter())
async def get_all_phone_for_change(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    phones = get_all_phone_by_masters(
        telegram_id=callback_query.from_user.id
    )

    if len(phones) == 0:
        await callback_query.answer(
            text=NOT_PHONES_ERROR,
            show_alert=True)

        return

    await bot.delete_message(
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id
    )

    messages_id = []
    for phone in phones:
        preview_text = PreviewPhone(
            phone=phone.number.international
        ).generate_preview_for_changes()

        message = await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text=preview_text,
            reply_markup=get_all_phone_for_changes_inl_kbd(
                phone_id=phone.id,
            ))

        messages_id.append(message.message_id)

    await state.update_data(messages_id=messages_id)


@contacts_for_master_phone_master_cb_query.callback_query(PhoneForChangesCbData.filter())
async def change_obtained_phone(
        callback_query: CallbackQuery,
        state: FSMContext,
        callback_data: PhoneForChangesCbData,
        bot: Bot
):
    state_data = await state.get_data()

    messages_id = state_data.get('messages_id')

    await bot.delete_messages(
        chat_id=callback_query.message.chat.id,
        message_ids=messages_id
    )

    await bot.send_message(
        text=ADD_PHONE,
        chat_id=callback_query.message.chat.id,
    )

    await state.set_state(ContactsAdminPhone.phone)
    await state.update_data(phone_id=callback_data.phone_id)


@contacts_for_master_phone_master_cb_query.callback_query(RemovePhoneCbData.filter())
async def get_all_phone_for_remove(
        callback_query: CallbackQuery,
        state: FSMContext,
        bot: Bot
):
    phones = get_all_phone_by_masters(
        telegram_id=callback_query.from_user.id
    )

    if len(phones) == 0:
        await callback_query.answer(
            text=NOT_PHONES_ERROR,
            show_alert=True)

        return

    await bot.delete_message(
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id
    )

    messages_id = []
    for phone in phones:
        preview_text = PreviewPhone(
            phone=phone.number.international
        ).generate_preview_for_delete()

        message = await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text=preview_text,
            reply_markup=get_all_phone_for_delete_inl_kbd(
                phone_id=phone.id,
            ))

        messages_id.append(message.message_id)

    await state.update_data(messages_id=messages_id)


@contacts_for_master_phone_master_cb_query.callback_query(PhoneForDeleteCbData.filter())
async def change_obtained_phone(
        callback_query: CallbackQuery,
        state: FSMContext,
        callback_data: PhoneForDeleteCbData,
        bot: Bot
):
    state_data = await state.get_data()

    messages_id = state_data.get('messages_id')

    await bot.delete_messages(
        chat_id=callback_query.message.chat.id,
        message_ids=messages_id
    )

    await callback_query.answer(text=SUCCESSFULLY, show_alert=True)

    remove_phone_by_phone_id(phone_id=callback_data.phone_id)

    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=ButtonAdminPanelOrMainMenu.ADMIN_PANEL,
        reply_markup=get_admin_main_menu_kbd()
    )

    await state.clear()
