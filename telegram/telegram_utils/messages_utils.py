from telegram.params.messages import CANNOT_MODIFY_OBSOLETE_LIST


async def cannot_modify_obsolete_list(callback_query):
    await callback_query.answer(text=CANNOT_MODIFY_OBSOLETE_LIST,
                                show_alert=True)
