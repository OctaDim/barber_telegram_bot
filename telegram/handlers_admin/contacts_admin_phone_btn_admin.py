from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from sqlalchemy_utils.types.phone_number import PhoneNumber

from telegram.filters.chat_types_filter import IsAdmin

from telegram.keyboard_inline.contacts_for_master_preview_phone import preview_phone_inl_kbd

from telegram.params.button_social_networks import PreviewPhone


contacts_admin_phone_btn_router = Router(name=__name__)
contacts_admin_phone_btn_router.message.filter(IsAdmin())


class ContactsAdminPhone(StatesGroup):
    phone = State()
    phone_id = State()


@contacts_admin_phone_btn_router.message(StateFilter(ContactsAdminPhone.phone))
async def preview_new_phone_master(
        message: Message,
        state: FSMContext
):
    phone = message.text

    phone = PhoneNumber(raw_number=phone, region='BY')

    if not phone.is_valid_number():
        await message.answer(text='Введите корректный номер телефона')
        return

    preview_text = PreviewPhone(phone=phone.international)

    await message.answer(
        text=preview_text.generate_preview(),
        reply_markup=preview_phone_inl_kbd()
    )

    await state.update_data(phone=phone.international)
